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

from spython.logger import bot
import os
import re
import sys

def pull(self, 
         image=None,
         name=None,
         pull_folder='',
         name_by_hash=False,
         name_by_commit=False,
         ext="simg"):

    '''pull will pull a singularity hub or Docker image
        
       Parameters
       ==========
       image: the complete image uri. If not provided, the client loaded is used
       pull_folder: if not defined, pulls to $PWD (''). If defined, pulls to
                    user specified location instead.

       Docker and Singularity Hub Naming
       ---------------------------------
       name: a custom name to use, to override default
       ext: if no name specified, the default extension to use.

       Singularity Hub Naming:
       ----------------------
       name_by_commit: name the image based on its commit
       name_by_hash: can be one of commit or hash, default is by image name

    ''' 
    self.check_install()
    cmd = self._init_command('pull')

    # No image provided, default to use the client's loaded image
    if image is None:
        image = self._get_uri()

    # If it's still None, no go!
    if image is None:
        bot.error('You must provide an image uri, or use client.load() first.')
        sys.exit(1)

    # Singularity Only supports shub and Docker pull
    if not re.search('^(shub|docker)://', image):
        bot.error("pull only valid for docker and shub. Use sregistry client.")
        sys.exit(1)           

    # Did the user ask for a custom pull folder?
    if pull_folder:
        self.setenv('SINGULARITY_PULLFOLDER', pull_folder)

    # Singularity Hub can name by commit or hash
    if image.startswith('shub://'):
        if name_by_commit is True:
            bot.debug("commit specified for image name")
            cmd.append("--commit")
        elif name_by_hash is True:
            bot.debug("file hash specified for image name")
            cmd.append("--hash")
        
    no_name = name_by_commit is False and name_by_hash is False

    # If we still don't have a custom name, base off of image uri.
    if name is None and no_name:
        name = "%s.%s" %(re.sub('^.*://','',image).replace('/','-'),ext)

    cmd = cmd + ["--name", name]
    
    cmd.append(image)
    bot.info(' '.join(cmd))
    self._run_command(cmd, capture=False)
    final_image = os.path.join(pull_folder, name)

    if os.path.exists(final_image):
        bot.info(final_image)
    return final_image