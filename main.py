import json
import argparse

from rapidpro_abtest_creator import RapidProABTestCreator
from sheets import CSVMasterSheetParser, GoogleMasterSheetParser
import logging

def main():
    parser = argparse.ArgumentParser(description='Apply FlowEdits/ABTests to a RapidPro JSON file.')
    parser.add_argument('input', help='RapidPro JSON file defining the input RapidPro flows.')
    parser.add_argument('output', help='RapidPro JSON file to write the output to.')
    parser.add_argument('master_sheets', nargs='+', help='Master sheet(s) referencing FlowEdits/ABTests. Either csv file(s) or a Google Sheet ID(s).')
    parser.add_argument('--format', required=True, choices=["csv", "google_sheets"], help='Format of the master sheet.')
    parser.add_argument('--logfile', help='File to log warnings and errors to.')
    parser.add_argument('--config', help='JSON config file.')
    args = parser.parse_args()

    if args.logfile:
        logging.basicConfig(filename=args.logfile, level=logging.WARNING, filemode='w')

    if args.config is not None:
        config = json.load(open(args.config, 'r'))
    else:
        config = {}

    if args.format == 'csv':
        sheet_parser = CSVMasterSheetParser(args.master_sheets)
    else:
        sheet_parser = GoogleMasterSheetParser(args.master_sheets)
    flow_edit_sheet_groups = sheet_parser.get_flow_edit_sheet_groups(config)
    rpx = RapidProABTestCreator(args.input)
    for flow_edit_sheets in flow_edit_sheet_groups:
        rpx.apply_abtests(flow_edit_sheets)
    rpx.export_to_json(args.output)




if __name__ == '__main__':
    main()
