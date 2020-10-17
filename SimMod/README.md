# SimMod - Python Simple Climate Model
Adapted version of the [SimMod model](https://github.com/hausfath/SimMod).

## Contributions
* The original model was updated to be compatible with the current package versions of the dependencies.
* Several bugs were fixed.
* Additional features (e.g., parameter sweep) and a more convenient user interface and output data structure are provided.

## Usage
0. Make sure you have numpy and pandas installed.
1. Open [`run_SimMod.py`](run_SimMod.py) in your editing tool of choice
2. Select desired parameters for RCP, carbon model, climate sensitivity, etc.
3. Run the model from your terminal via
    ```bash
    python run_SimMod.py
    ```
4. Results will be saved in `.csv` format in a newly created `SimMod/results/<timestamp>/` folder. The configuration is saved alongside.

*Note: Use the [`run_SimMod_sweep.py`](run_SimMod_sweep.py) script for running a parameter sweep for the climate feedback parameter.* 

## Notes
* The BEAM carbon model overestimates 2100 atmospheric CO2 concentrations
by \~25% relative to RCP scenarios. Using the pulse response carbon model
is recommended for the time being. The latest BEAM model can be found [here](https://github.com/RDCEP/BEAM-carbon/find/master)

* The BEAM Carbon model needs to be installed separately. This can be done via
    ```bash
    cd beam_carbon
    python setup.py install
    ```
  For more details have a look at the [BEAM Carbon README](beam_model/README.md)

## CSV Legend
### Model Inputs
Legend for the `emissions/rcp_*_data.csv` files.

| Label                 | Description                                                           |
|-----------------------|-----------------------------------------------------------------------|
| year                  | Calendar Year                                                         |
| ch4_emissions_tg      | Anthropogenic emissions of CH4 by timestep from selected RCP [in tg]  |
| n2o_emissions_tg      | Anthropogenic emissions of N2O by timestep from selected RCP [int pg] |
| c_emissions_pg        | Anthropogenic emissions of C by timestep from selected RCP [int pg]   |
| co2_concentration_ppm | CO2 concentrations [in ppm]                                           |
| ch4_concentration_ppb | CH4 concentrations [in ppb]                                           |
| n2o_concentration_ppb | N2O concentrations [in ppb]                                           |
| co2_forcing_wm2       | Radiative forcing of CO2 [in W/m^2]                                   |
| ch4_forcing_wm2       | Radiative forcing of CH4 [in W/m^2]                                   |
| n2o_forcing_wm2       | Radiative forcing of N2O [in W/m^2]                                   |
| total_forcing_wm2     | Total anthropogenic forcing [in W/m^2]                                |

### Model Outputs
Legend for the `results/<timestamp>/results.csv` files.

| Label              | Description                                                           |
|--------------------|-----------------------------------------------------------------------|
| date               | Count of timesteps since the specified starting point                 |
| year               | Calendar Year                                                         |
| co2_pg             | Anthropogenic emissions of CO2 by timestep from selected RCP [in tg]  |
| ch4_tg             | Anthropogenic emissions of CH4 by timestep from selected RCP [in tg]  |
| n2o_tg             | Anthropogenic emissions of N2O by timestep from selected RCP [int pg] |
| co2_forcing_rcp    | RCP data for the radiative forcing of CO2 [in W/m^2]                  |
| ch4_forcing_rcp    | RCP data for the radiative forcing of CH4 [in W/m^2]                  |
| n2o_forcing_rcp    | RCP data for the radiative forcing of N2O [in W/m^2]                  |
| total_forcing_rcp  | RCP data for the total anthropogenic forcing [in W/m^2]               |
| rcp_co2_ppm        | RCP data for the CO2 concentrations [in ppm]                          |
| rcp_ch4_ppb        | RCP data for the CH4 concentrations [in ppb]                          |
| rcp_n2o_ppb        | RCP data for the N2O concentrations [in ppb]                          |
| co2_pg_atm         | Atmospheric CO2 [in pg]                                               |
| ch4_tg_atm         | Atmospheric CH4 [in tg]                                               |
| n2o_tg_atm         | Atmospheric N2O [in tg]                                               |
| co2_ppm            | Atmospheric CO2 concentration [in ppm]                                |
| ch4_ppb            | Atmospheric CH4 concentration [in ppb]                                |
| n2o_ppb            | Atmospheric N2O concentration [in ppb]                                |
| co2_forcing        | Radiative forcing of CO2 [in W/m^2]                                   |
| ch4_forcing        | Radiative forcing of CH4 [in W/m^2]                                   |
| n2o_forcing        | Radiative forcing of N2O [in W/m^2]                                   |
| total_forcing_ghg  | Total radiative forcing from GHGs (CO2, CH4, N2O) [in W/m^2]          |
| rcp_nonghg_forcing | Non-GHG radiative forcing (taken from RCP) [in W/m^2]                 |
| total_forcing      | Sum of GHG and non-GHG forcing [in W/m^2]                             |
| t_os               | Aquaworld transient temperature response (no land fraction) [in K]    |
| t_eq               | Equilibrium temperature reponse (no oceans) [in K]                    |
| t_s                | Transient temperature response (land/ocean) [in K]                    |

## License
[The original code](https://github.com/hausfath/SimMod) is distributed under the Apache 2 License.
