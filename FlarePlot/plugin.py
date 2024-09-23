"""
Plugin entrypoint
"""

from HorusAPI import Plugin

# Configs
from Config.netcdf import netcdf_config_block
from Config.conda import conda_config_block

# Blocks
from Blocks.GetStaticContacts import get_contacts_block
from Blocks.GetContactFreqs import generate_freqs_block
from Blocks.GetResilabels import generate_resilabels_block
from Blocks.GetContactFingerprints import generate_contact_fingerprints_block
from Blocks.GetContactFlare import generate_flareplot_block
from Blocks.GetDynamicContacts import generate_dynamic_contacts_block

# Pages
from Pages.flareplot_page import flareplot_page

plugin = Plugin()

# Configs
plugin.addConfig(netcdf_config_block)
plugin.addConfig(conda_config_block)

# Blocks
plugin.addBlock(get_contacts_block)
plugin.addBlock(generate_freqs_block)
plugin.addBlock(generate_resilabels_block)
plugin.addBlock(generate_contact_fingerprints_block)
plugin.addBlock(generate_flareplot_block)
plugin.addBlock(generate_dynamic_contacts_block)

# Pages
plugin.addPage(flareplot_page)
