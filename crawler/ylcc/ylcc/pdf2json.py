# -*- coding: utf-8 -*-
import os
import csv
import json
import codecs
import re

def get_link(filename):
	data_file = 'meetings.json'
	if not os.path.exists(data_file):
		print "run scapy to build meeting.json"
		exit()
	with open(data_file) as data:
		meeting_records = json.load(data)

	for meeting in meeting_records:
		if filename in meeting['download_url']:
			return meeting['download_url']


def get_proposed_name(proposed_by):
	# remove single extra space
	proposed_by = re.sub('\s(?=\S{3})', '', proposed_by)

	for i in xrange(0, len(proposed_by), 3):
		name = proposed_by[i:i+3]
		if ('  ' in name):
			name = proposed_by[i:i+5]
			i = i+2
			yield name.replace('  ', '')
		else:
			if (len(name) == 3):
				yield proposed_by[i:i+3]


def generate_id(filename, count):
	return filename + "{:0>3d}".format(count)


def covert2csv(rawdata_dir):
	for root, subdir, files in os.walk(rawdata_dir):
		for file in files:
			if file.endswith(".pdf"):
				#pdffile = rawdata_dir + "/" + file
				pdffile = os.path.join(root, file)
				csvfile = pdffile[:-4] + ".csv"
				if (not os.path.isfile(csvfile)):
					tabula_cmd = "jruby %s -r -p all -o %s %s" % (tabula_script, csvfile, pdffile)
					print tabula_cmd
					os.system(tabula_cmd)


def csv2json(rawdata_dir):
	all_bills = []
	all_billsfile = codecs.open("../../../data/ylcc/bills.json", 'w', 'utf-8')

	for root, subdir, files in os.walk(rawdata_dir):
		for file in files:
			bill_count = 0
			if file.endswith(".csv"):
				#csvfile = rawdata_dir + "/" + file
				csvfile = os.path.join(root, file)
				fieldnames = ("bill_no", "proposed_by", "abstract", "committee_motion", "councile_motion")
				reader = csv.DictReader(open(csvfile, 'r'), fieldnames)
				bills = json.dumps([row for row in reader], indent=4, sort_keys=True, ensure_ascii=False)
				bills = json.loads(bills)

				for bill in bills:
					if bill['proposed_by'] != u'提案人':
						bill_count += 1
						bill['election_year'] = 2009
						bill['links'] = get_link(os.path.basename(csvfile[:-4]))
						bill['county'] = u'雲林縣'
						bill['last_action'] = ''
						bill['petitioned_by'] = ''
						bill['methods'] = ''
						if bill['committee_motion']:
							committee_motion = bill['committee_motion'].replace(" ", "")
							del bill['committee_motion']
						if bill['councile_motion']:
							councile_motion = bill['councile_motion'].replace(" ", "")
							del bill['councile_motion']
						bill['motions'] = [
							{"date": "", "motion": u'審查意見', "resolution": committee_motion},
							{"date": "", "motion": u'大會議決', "resolution": councile_motion}
						]
						bill['proposed_by'] = list(get_proposed_name(bill['proposed_by']))
						bill['id'] = generate_id(os.path.basename(csvfile[:-4]), bill_count)
						all_bills.append(bill)

	all_bills = json.dumps(all_bills,indent=4, sort_keys=True, ensure_ascii=False)
	all_billsfile.write(all_bills)


if __name__ == '__main__':
	script_path = os.path.dirname(os.path.abspath(__file__))
	os.chdir(script_path)

	tabula_script = "/Users/ericj/.rbenv/versions/jruby-1.7.11/bin/tabula"
	rawdata_dir = script_path + "/meeting_minutes"
	print rawdata_dir
	covert2csv(rawdata_dir)
	csv2json(rawdata_dir)
