#!/usr/bin/python

from roscompile.people_management import fix_people, fix_licenses
from roscompile.config import CFG

def roscompile_one(package):
    roscompile([package])

def roscompile(pkgs):
    if CFG.should('update_manifest'):
        if CFG.should('check_names'):
            fix_people(pkgs)
        if CFG.should('check_licenses'):
            fix_licenses(pkgs)

    for package in pkgs:
        if CFG.should('update_manifest'):
            package.update_manifest()

        if CFG.should('update_cmake'):
            package.update_cmake()

        if CFG.should('remove_useless'):
            package.remove_useless()

        if CFG.should('generate_setup_py'):
            package.generate_setup()

        if CFG.should('check_plugins'):
            package.check_plugins()

        if CFG.should('check_permissions'):
            package.check_permissions()
