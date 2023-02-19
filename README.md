# Meeting Cost Calculator for University of Michigan® Staff REST API

## Summary

This application supplies a REST API for finding University of Michigan staff members and calculating the cost to the
University of meeting with them.

## Description

The purpose of this application is to provide a back-end tool for finding particular University of Michigan staff and
calculating the cost of one or more of them attending any particular meeting of any arbitrary length. An example
front-end application designed to tap this API is available [here](https://github.com/whorvath2/um_mcc_ui).

## Inspiration

Meeting invitations are often sent without an agenda, which makes their business value very difficult to determine.
Knowing what they will cost brings a new level of accountability to the organizer.

## Technical Details

This is a [Flask](https://flask.palletsprojects.com/en/2.2.x/)-based REST API written
in [Python](https://www.python.org). It
leverages [publicly available salary data](https://www.dropbox.com/s/ti4iff026agzpak/salary-disclosure-2022.pdf?dl=0) to
enable the search and selection of meeting attendees and the calculation of meeting cost.
It [exposes endpoints](src/co/deability/um_mcc/controller.py) for a health check; searching for staff by name, title,
and department; and for determining the cost of a meeting via a client-supplied list of staff members and the meeting
length in minutes.

## Dependencies

This application is designed to be [containerized](Dockerfile) for use in a virtual machine, such as that supplied
by [podman](https://podman.io/getting-started/installation). Dependencies and other considerations are handled in the
containerization process automatically.

## Building

To build the API using podman, open a terminal session in this directory, then build the image and create the container:

```
podman build --tag um_mcc_image .
podman create --name=um_mcc_api localhost/um_mcc_image:latest
```

## Usage

To launch the application in the same terminal session:

```
podman start um_mcc_api
```

To verify the API is
available, [open your browser to the health check endpoint at localhost:8000/um_mcc](http://localhost:8000/um_mcc).

An OpenAPI specification will be available in a future release.

## Version

1.1.1

## Disclaimers

## Disclaimers

**THIS APPLICATION IS NEITHER ENDORSED BY NOR ASSOCIATED WITH THE UNIVERSITY OF MICHIGAN®.**

University of Michigan, UM, U-M, and U of M are trademarks™ or registered® trademarks of the University of Michigan. Use
of them does not imply any affiliation with or endorsement by the University of Michigan. For all other
disclaimers, [see the LICENSE file in this repository](LICENSE).

_Thank you termly.io for the disclaimer language._

_Copyright ©️ 2023 William L Horvath II_