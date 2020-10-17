"""Run the SimMod model"""
import os
from datetime import datetime

import pandas as pd
import numpy as np
import yaml

from constants import *
from emissions_parser import emissions
from concs_pulse_decay import pulse_decay_runner
from radiative_forcing import calc_radiative_forcing
from heat_diffusion import continuous_diffusion_model

# .............................................................................
# SimMod configuration. Adjust the model parameters here.

OUT_DIR = "results"
FILE_EXT = ".csv"

CFG_SIMMOD = dict(
    # SimMod Parameters
    run_start_year = 1765.,          # Run start year
    run_end_year = 2500.,            # Inclusive of end year
    dt = 1, #/ 100.                  # years
    rcp = '8.5',                     # RCP scenario
    add_start = 0,
    add_end = 0,
    c_add = 0,
    ch4_add = 0,
    n2o_add = 0,

    carbon_model = 'pulse_response', # 'pulse response' or 'BEAM'
    normalize_2000_conc = False,     # Normalize concentrations to historical year-2000 values
    c_sens = 1.25,                   # Climate feedback parameter (T = F / LAMBDA)

    cfg_beam = dict(
        # BEAM Model Settings (when relevant)
        SUBSTEPS = 100,              # Break each timestep into this many substeps
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
    Run the various parts of SimMod and save the results.
    """
    run_years = (run_end_year - run_start_year + 1)
    emission_vals = emissions(run_start_year, run_end_year, dt, rcp, 
                              add_start, add_end, c_add, ch4_add, n2o_add)
    conc = pulse_decay_runner(run_years, dt, emission_vals)

    if carbon_model == 'BEAM':
        try:
            from beam_carbon.beam import BEAMCarbon
        except ImportError as err:
            raise RuntimeError("No BEAMCarbon model found! Please run the "
                               "installation procedure for the BEAMCarbon "
                               "model in '/beam_carbon/'.") from err

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

    # Run the model
    results = run_simmod(**CFG_SIMMOD)

    # Save the results
    filename = "results" + FILE_EXT
    results.to_csv(os.path.join(out_dir, filename))

    # Save the configuration
    cfg_path = os.path.join(out_dir, 'configuration.yml')
    with open(cfg_path, 'w') as file:
        yaml.dump(CFG_SIMMOD, file, default_flow_style=False)
