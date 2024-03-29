"""
Generate BIND9 db files from yaml. 
"""

import yaml 
import jinja2 
import datetime 
import ipaddress
import glob 
import pathlib 
import os 
import argparse


def reverse(hosts, network):
	rval = ''
	rzone = ipaddress.ip_network(network)
	for host in hosts:
		for addr in hosts[host]:
			try:
				ip = ipaddress.ip_address(addr)
				if ip in rzone:
					if ip.version == 4:
						hostaddr = str(ip).split('.')[3]
					else:
						hostaddr = '.'.join(reversed(ip.exploded.replace(':', '')[16:]))
					rval += f"{hostaddr} IN PTR {host}.cis.cabrillo.edu.\n"	
			except:
				"""not an IP address""" 

	return(rval)


def fwd(hosts, role):
	rval = ""
	for host in hosts:
		for addr in hosts[host]:
			try:
				ip = ipaddress.ip_address(addr)
				if ((role == 'external' and (ip.version == 6 or not ip.is_private)) or 
					(role == 'internal' and (ip.version == 6 or ip.is_private))):
					if ip.version == 4:
						rval += f"{host} IN A {ip}\n"
					else:
						rval += f"{host} IN AAAA {ip}\n"
			except:
				# This is a name 
				rval += f"{host} IN CNAME {addr}\n"	

	return rval 


def subdomain(domains, role):
	"""Make NS and glue records.""" 
	rval = ""
	if domains is not None:
		for d in domains:
			if d['name'].endswith('.') and role == 'external':
				continue
			for i, ns in enumerate(d['ns']):
				try:
					# IP address needs a glue record
					ip = ipaddress.ip_address(ns)
					rval += f"""{d['name']} IN NS ns{i+1}.{d['name']}\n"""
					if ip.version == 4:
						rval += f"""ns{i+1}.{d['name']} IN A {ip}\n"""
					else:
						rval += f"""ns{i+1}.{d['name']} IN AAAA {ip}\n"""
				except Exception as e:
					# Assume the glue record exists
					rval += f"""{d['name']} IN NS {ns}\n"""
	return rval 


def main():
	parser = argparse.ArgumentParser(description='Generate zone files from templates')
	parser.add_argument('--dry-run', action='store_true', help='Print files instead of writing them.')
	parser.add_argument('path', default="./source", nargs='?', help='The path to the configuration files [default=./source]')
	args = parser.parse_args()

	inv = {}
	path = pathlib.Path(args.path)
	for source in sorted(path.glob('*.yaml')):
		print(f"Loading {source}")
		with open(source) as f:
			y = yaml.load(f, Loader=yaml.Loader)
			for k in list(inv.keys()):
				if k in y:
					inv[k].update(y[k])
			for k in y:
				if k not in inv:
					inv[k] = y[k]

	now = datetime.datetime.now()
	inv['soa'] = inv['soa'].format(serial=f'{now:%Y%m%d}{inv["serial"]}')

	if not args.dry_run:
		os.mkdir('build')

	for templfile in glob.glob('templates/db.*'):
		print(f"Building template {templfile}")
		with open(templfile) as f:
			template = jinja2.Template(f.read())	
			output = "build/" + pathlib.Path(templfile).name
			rendered = template.render(inv, 
					reverse=reverse,
					fwd=fwd,
					subdomain=subdomain,
				)
			print(rendered)
			if not args.dry_run:
				with open(output, 'w') as of:
					of.write(rendered)

if __name__ == '__main__':
	main()
