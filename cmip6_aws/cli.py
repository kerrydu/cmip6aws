"""Command-line interface for cmip6_aws."""
import argparse
import sys
from .cmip6_aws import CMIP6


def list_command(args):
    """List available CMIP6 data options."""
    cmip6 = CMIP6()
    
    if args.type == 'models':
        print("Available Models:")
        for model in sorted(cmip6.model()):
            print(f"  - {model}")
    
    elif args.type == 'scenarios':
        if args.model:
            scenarios = cmip6.scenario(args.model)
        else:
            scenarios = cmip6.scenario()
        print(f"Available Scenarios{' for model ' + args.model if args.model else ''}:")
        for scenario in sorted(scenarios):
            print(f"  - {scenario}")
    
    elif args.type == 'variables':
        if args.model:
            cmip6.scenario(args.model)
        if args.scenario:
            variables = cmip6.variable(args.scenario)
        else:
            variables = cmip6.variable()
        print(f"Available Variables{' for scenario ' + args.scenario if args.scenario else ''}:")
        for variable in sorted(variables):
            print(f"  - {variable}")
    
    elif args.type == 'years':
        if args.model:
            cmip6.scenario(args.model)
        if args.scenario:
            cmip6.variable(args.scenario)
        if args.variable:
            years = cmip6.year(args.variable)
        else:
            years = cmip6.year()
        print(f"Available Years/Versions{' for variable ' + args.variable if args.variable else ''}:")
        for year in sorted(years):
            print(f"  - {year}")
    
    elif args.type == 'all':
        print("\n=== Available Models ===")
        for model in sorted(cmip6.model()):
            print(f"  - {model}")
        
        cmip6.reset()
        print("\n=== Available Scenarios ===")
        for scenario in sorted(cmip6.scenario()):
            print(f"  - {scenario}")
        
        cmip6.reset()
        print("\n=== Available Variables ===")
        for variable in sorted(cmip6.variable()):
            print(f"  - {variable}")
        
        cmip6.reset()
        print("\n=== Available Years/Versions ===")
        years = cmip6.year()
        # Show only first 10 as there are many
        for year in sorted(years)[:10]:
            print(f"  - {year}")
        print(f"  ... and {len(years) - 10} more")


def download_command(args):
    """Download CMIP6 data."""
    cmip6 = CMIP6()
    
    # Parse lat/lon ranges
    lat_range = [float(x) for x in args.lat_range.split(',')]
    lon_range = [float(x) for x in args.lon_range.split(',')]
    
    if len(lat_range) != 2 or len(lon_range) != 2:
        print("Error: lat-range and lon-range must each contain exactly 2 values (min,max)")
        sys.exit(1)
    
    # Parse years (can be single year or comma-separated list)
    if ',' in args.years:
        years = args.years.split(',')
    else:
        years = [args.years]
    
    print(f"\nDownloading data with parameters:")
    print(f"  Model: {args.model}")
    print(f"  Scenario: {args.scenario}")
    print(f"  Variable: {args.variable}")
    print(f"  Years: {years}")
    print(f"  Latitude range: {lat_range}")
    print(f"  Longitude range: {lon_range}")
    print(f"  Output directory: {args.output}\n")
    
    try:
        cmip6.down(
            outputdir=args.output,
            model=args.model,
            scenario=args.scenario,
            variable=args.variable,
            year=years,
            latminmax=lat_range,
            lonminmax=lon_range
        )
        print("\nDownload completed successfully!")
    except Exception as e:
        print(f"\nError during download: {str(e)}")
        sys.exit(1)


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='CMIP6 AWS Data Tool - Download and explore CMIP6 climate data from NEX-GDDP-CMIP6',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # List all models
  cmip6_aws list models
  
  # List scenarios for a specific model
  cmip6_aws list scenarios --model CESM2
  
  # List all available data types
  cmip6_aws list all
  
  # Download data
  cmip6_aws download --model CESM2 --scenario ssp585 --variable pr \\
                     --years 2015v1.1,2016v1.1 --lat-range 5,55 \\
                     --lon-range 55,56 --output ./data
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available CMIP6 data options')
    list_parser.add_argument(
        'type',
        choices=['models', 'scenarios', 'variables', 'years', 'all'],
        help='Type of data to list'
    )
    list_parser.add_argument('--model', help='Filter by model name')
    list_parser.add_argument('--scenario', help='Filter by scenario')
    list_parser.add_argument('--variable', help='Filter by variable')
    list_parser.set_defaults(func=list_command)
    
    # Download command
    download_parser = subparsers.add_parser('download', help='Download CMIP6 data')
    download_parser.add_argument('--model', required=True, help='Model name (e.g., CESM2)')
    download_parser.add_argument('--scenario', required=True, help='Scenario (e.g., ssp585)')
    download_parser.add_argument('--variable', required=True, help='Variable (e.g., pr for precipitation)')
    download_parser.add_argument('--years', required=True, help='Year(s) with version (e.g., 2015v1.1 or 2015v1.1,2016v1.1)')
    download_parser.add_argument('--lat-range', required=True, help='Latitude range as min,max (e.g., 5,55)')
    download_parser.add_argument('--lon-range', required=True, help='Longitude range as min,max (e.g., 55,56)')
    download_parser.add_argument('--output', required=True, help='Output directory for downloaded files')
    download_parser.set_defaults(func=download_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == '__main__':
    main()
