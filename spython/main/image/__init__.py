'''

Copyright (C) 2018 The Board of Trustees of the Leland Stanford Junior
University.
Copyright (C) 2018 Vanessa Sochat.

This program is free software: you can redistribute it and/or modify it
under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or (at your
option) any later version.

This program is distributed in the hope that it will be useful, but WITHOUT
ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Affero General Public
License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

'''

from .generate import RobotNamer

def generate_image_commands():
    ''' The Image client holds the Singularity image command group, mainly
        deprecated commands (image.import) and additional command helpers
        that are commonly use but not provided by Singularity

        The levels of verbosity (debug and quiet) are passed from the main
        client via the environment variable MESSAGELEVEL.
    '''

    class ImageClient:
        group = "image"

    from .utils import ( compress, decompress )
    from .create import create
    from .importcmd import importcmd
    from .export import export

    ImageClient.create = create
    ImageClient.imprt = importcmd
    ImageClient.export = export
    ImageClient.decompress = decompress
    ImageClient.compress = compress
 
    cli = ImageClient()
    return cli

image_group = generate_image_commands()