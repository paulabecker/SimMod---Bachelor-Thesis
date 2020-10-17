"""Run a parameter sweep for the SimMod model"""
import os
from datetime import datetime
import copy

import pandas as pd
import xarray as xr
import numpy as np
import yaml
from tqdm import tqdm

from constants import *
from emissions_parser import emissions
from concs_pulse_decay import pulse_decay_runner
from beam_carbon.beam import BEAMCarbon
from radiative_forcing import calc_radiative_forcing
from heat_diffusion import continuous_diffusion_model

# .............................................................................

OUT_DIR = "results"
FILE_EXT = ".nc"

C_SENS_MEAN = 1.25
C_SENS_STD = 0.5
N_SAMPLES = 1000
CLIMATE_SENSITIVITIES = np.random.randn(N_SAMPLES)*C_SENS_STD + C_SENS_MEAN

CFG_SIMMOD = dict(
    run_start_year = 1765.,
    run_end_year = 2500.,
    dt = 1,
    rcp = '8.5',
    add_start = 0,
    add_end = 0,
    c_add = 0,
    ch4_add = 0,
    n2o_add = 0,

    carbon_model = 'pulse_response',
    normalize_2000_conc = False,
    c_sens = 1.25,

    cfg_beam = dict(
        SUBSTEPS = 100,
        INIT_MAT = 596.,             # In GtC; 596 = preindustrial; 809 = 2005
        INIT_MUP = 713.,             # In GtC; 713 = preindustrial; 725 = 2005
        INIT_MLO = 35625.,           # In GtC; 35625 = preindustrial; 35641 = 2005
        temperature_dependent = True
    )
)

# ............................................................................

def run_simmod(*, run_start_year, run_end_year,
                  dt,
                  rcp,
                  add_start, add_end, c_add, ch4_add, n2o_add,
                  carbon_model,
                  cfg_beam,
                  normalize_2000_conc,
                  c_sens):
    """
    Run the various parts of SimMod and export images and CSV files.
    """
    run_years = (run_end_year - run_start_year + 1)
    emission_vals = emissions(run_start_year, run_end_year, dt, rcp, 
                              add_start, add_end, c_add, ch4_add, n2o_add)
    conc = pulse_decay_runner(run_years, dt, emission_vals)

    if carbon_model == 'BEAM':
        beam = BEAMCarbon()
        beam._temperature_dependent = cfg_beam['temperature_dependent']
        beam._initial_carbon = np.array([cfg_beam['INIT_MAT'],
                                         cfg_beam['INIT_MUP'],
                                         cfg_beam['INIT_MLO']])
        beam.intervals = cfg_beam['SUBSTEPS']
        beam.time_step = dt
        beam.emissions = emission_vals['co2_pg'] / C_TO_CO2
        beam_results = pd.melt(beam.run()[0:1])
        conc['co2_ppm'] = beam_results['value'] * PGC_TO_MOL * 1e6 / MOLES_IN_ATMOSPHERE

    if normalize_2000_conc == True:
        conc['co2_ppm'] = (
            conc['co2_ppm'] - 
            conc.loc[conc['year'] == 2000, 'co2_ppm'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_co2_ppm'].min()
        )
        conc['ch4_ppb'] = (
            conc['ch4_ppb'] - 
            conc.loc[conc['year'] == 2000, 'ch4_ppb'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_ch4_ppb'].min()
        )
        conc['n2o_ppb'] = (
            conc['n2o_ppb'] - 
            conc.loc[conc['year'] == 2000, 'n2o_ppb'].min() +
            emission_vals.loc[emission_vals['year'] == 2000, 'rcp_n2o_ppb'].min()
        )

    forcing = calc_radiative_forcing(conc)
    warming = continuous_diffusion_model(forcing, run_years, dt, c_sens)
    return warming

if __name__ == '__main__':
    # Create results folder with current timestamp
    tag = datetime.now().strftime("%y%m%d-%H%M%S")
    tag += ("-" + CFG_SIMMOD['carbon_model'].replace(" ", "_")
            + "-rcp" + CFG_SIMMOD['rcp'].replace(".", ""))

    out_dir = os.path.join(OUT_DIR, tag)
    os.makedirs(out_dir)

    # Run the model for different climate sensitivities
    results_single = []
    for c_sens in tqdm(CLIMATE_SENSITIVITIES,
                       desc="Climate Sensitivity Sweep"):
        cfg_simmod = copy.deepcopy(CFG_SIMMOD)
        cfg_simmod['c_sens'] = c_sens
        output = run_simmod(**cfg_simmod)
        output = xr.Dataset.from_dataframe(output)
        output = (output.assign({'c_sens': c_sens})
                        .set_coords('c_sens').expand_dims('c_sens'))
        results_single.append(output)

    results = xr.concat(results_single, dim='c_sens')

    # Save the results
    filename = "results" + FILE_EXT
    results.to_netcdf(os.path.join(out_dir, filename))

    # Save the configuration
    cfg_path = os.path.join(out_dir, 'configuration.yml')
    cfg_save = copy.deepcopy(CFG_SIMMOD)
    cfg_save['c_sens'] = list(CLIMATE_SENSITIVITIES)
    with open(cfg_path, 'w') as file:
        yaml.dump(cfg_save, file, default_flow_style=False)
