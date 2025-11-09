# cmip6_aws


[![image](https://img.shields.io/pypi/v/cmip6_aws.svg)](https://pypi.python.org/pypi/cmip6_aws)
[![image](https://img.shields.io/conda/vn/conda-forge/cmip6_aws.svg)](https://anaconda.org/conda-forge/cmip6_aws)


**Download data from NASA Earth Exchange Global Daily Downscaled Projections (NEX-GDDP-CMIP6)**


-   Free software: MIT license
-   Documentation: https://advancehs.github.io/cmip6_aws
    

## Installation

```bash
pip install cmip6-aws
```

## Command Line Usage

After installation, you can use the `cmip6_aws` command to explore and download CMIP6 climate data.

### List Available Data

**List all models:**
```bash
cmip6_aws list models
```

**List scenarios for a specific model:**
```bash
cmip6_aws list scenarios --model CESM2
```

**List variables for a specific scenario:**
```bash
cmip6_aws list variables --model CESM2 --scenario ssp585
```

**List years/versions for a specific variable:**
```bash
cmip6_aws list years --model CESM2 --scenario ssp585 --variable pr
```

**List all available options:**
```bash
cmip6_aws list all
```

### Download Data

Download CMIP6 data with geographic filtering:

```bash
cmip6_aws download \
  --model CESM2 \
  --scenario ssp585 \
  --variable pr \
  --years 2015v1.1,2016v1.1 \
  --lat-range 5,55 \
  --lon-range 55,56 \
  --output ./data
```

**Parameters:**
- `--model`: Model name (e.g., CESM2, ACCESS-CM2)
- `--scenario`: Climate scenario (e.g., ssp585, ssp245, historical)
- `--variable`: Climate variable (e.g., pr=precipitation, tas=temperature)
- `--years`: Year(s) with version, comma-separated for multiple years (e.g., 2015v1.1 or 2015v1.1,2016v1.1)
- `--lat-range`: Latitude range as min,max (e.g., 5,55)
- `--lon-range`: Longitude range as min,max (e.g., 55,56)
- `--output`: Output directory for downloaded files

## Python API

You can also use cmip6_aws as a Python library:

```python
from cmip6_aws.cmip6_aws import CMIP6

# Initialize
cmip6 = CMIP6()

# List available models
models = cmip6.model()
print(models)

# Filter by model and list scenarios
scenarios = cmip6.scenario("CESM2")
print(scenarios)

# Filter by scenario and list variables
variables = cmip6.variable("ssp585")
print(variables)

# Filter by variable and list years
years = cmip6.year("pr")
print(years)

# Download data
cmip6.down(
    outputdir="./data",
    model="CESM2",
    scenario="ssp585",
    variable="pr",
    year=["2015v1.1", "2016v1.1"],
    latminmax=[5, 55],
    lonminmax=[55, 56]
)
```