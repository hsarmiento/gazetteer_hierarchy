#!/usr/bin/python3
import sys
# import os

def search_region_code_data(country_code,region_file,gazetteer_file):
	l = []
	with open(region_file) as region_f:
		for line_region in region_f:
			code_r = line_region.strip().lower()
			with open(gazetteer_file) as gazetteer_f:
				for line_gaz in gazetteer_f:
					list_gaz = line_gaz.strip().lower().split("\t")
					if list_gaz[6] == "a" and list_gaz[11] == code_r:
						if 'adm2' in list_gaz[7] and list_gaz[10] == country_code:
							t = (list_gaz[1],code_r,country_code,list_gaz[4],list_gaz[5],list_gaz[1].split()[-1])
							l.append(t)
							break
		return l

def write_sql_file(list_data,final_file):
	with open(final_file,"w") as final_f:
		for reg,reg_code,country_code,lat,lon,last_word in list_data:
			t = """INSERT IGNORE INTO regions (region, region_code, country_code, lat, lon, last_word)
                    values ('%s', '%s', '%s', '%s', '%s', '%s');
                \n\n
                """ %(reg,reg_code.upper(),country_code.upper(),lat,lon,last_word)
    		
			final_f.write(t)
			



#argv in lower
if __name__ == "__main__":
	country_code = sys.argv[1]
	region_file = sys.argv[2]
	gazetteer_file = sys.argv[3]
	final_file = sys.argv[4]
	list_codes_data = search_region_code_data(country_code,region_file,gazetteer_file)
	print(len(list_codes_data))
	# write_sql_file(list_codes_data,final_file)