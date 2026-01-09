
#---------------------------------------------------------------#
# DUCKWEED LABS
# This file serves as a .txt for edits and tests done by 
# the team members leading up to the physical integration
# of the HMI system. It is split by date and details specific
# information about what was done, and plans moving forward.
#---------------------------------------------------------------#


#---------------------------------------------------------------#
# JANUARY 3rd
# - Successfully updated tailnet website to allow access from
#   HMI team's professional emails to circumvent dual-factor
#   authentication challenge.
#
# - Confirmed functionality of all sensors from implementation
#   the first week of December in Gainseville, FL. 
#
# - Determined programming as-is with basic windows ssh will
#   not allow users to view the data output outside of termimal
#   (e.g., matplotlib outputs), and may require a separate 
#   supporting software, such as visual studio code.
#
#   OS
#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
# JANUARY 4th
# - Compiled individual programs into main singular program 
#   titled "dw_prog_v0" for creating functions that are modular
#   for multiple use cases.
# - These functions are split between sens_x_setup and
#   sens_x_read, where x refers to the specific sensor. 
#
#   OS
#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
# JANUARY 5th
# - Created larger general functions for sens_setup() and
#   sens_read() that setup or read data for all sensors
#   respectively.
# - STEPS TO IMPLEMENT FILE SYSTEM:
#   1. Make test file to work with time library. Convert to EST
#      given our team's testing dominance on the east coast.
#      COMPLETE
#   2. Make test file to work with data manipulation and
#      analysis. I am going to use the pandas library but if 
#      anyone (probably Candela) has a preferred extension just
#      feel free to make a note of it here.
#      COMPLETE
#   3. Utilize time and pandas libraries inside of the main file
#      (as in, saving dw_prog_v0 and place it into legacy file,
#      which I will do before I log off) and continue working on
#      these topics in a copy of the file called "dw_prog_v1".
#       - Legacy file = "dw_legacy_prog"
#
#   dw_legacy_pro - DUCKWEED_LEGACY_PROGRAMS
#   -  Legacy versions of main program (v0, v1, v2...).
#   dw_test_prog  - DUCKWEED_TEST_PROGRAMS
#   -  Test programs for individual sensors & initialization.
#   dw_poor_prog  - DUCKWEED_POOR_PROGRAMS
#   -  Programs that were added but do not actively run (bugged).
#
#   OS
#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
# JANUARY 6th
# - Installed the pandas library to the RPi for data handling
#   and transmission to a central log for the team to use for
#   analysis. 
# - Created DW_TIME_FUNCT.py to handle time acquisition with
#   eastern time zone bias in the log.
# - Created DW_FILE_FUNCT.py to handle sensor data acquisition
#   and data transmission to the central log, either reads from
#   all sensors or reads from single sensors at a time.
# - Standardized file naming convention:
#                 ENTITY_SUBJECT_ACTION
#   - Ex.: DW_FILE_FUNCT - Duckweed Labs, File System, Functions
#
# IMPORTANT NOTES
# - Splitting up the central duckweed code into multiple programs
#   improves readability, but does mean different versions of
#   the duckweed code may be saved as files now holding each
#   DW_xx_xx program as opposed to a single v1.py, v2.py...
# - Need to determine how data will be saved for the thermal
#   cameras since they're main thing is the pyplot.
# - Existing things to get done are determine method for i2c
#   connection of second thermal camera, working on the gui
#   (basic background, interactable buttons {I would suggest
#   Candela to try working on this because she has the 
#   touchscreen where data is output, whereas I may need to 
#   get VScode to see the output) and watch videos on RPi
#   clustering determining whether we'll use both RPis on
#   this prototype.
#
#   OS
#
#---------------------------------------------------------------#

#---------------------------------------------------------------#
# JANUARY 8th
# - Successfully got two thermal cameras on the singular rpi
#   while circumventing physical i2c multiplexer challenge.
# - Began GUI programming with sensor startup. Identified 
#   challenge where sens_setup() may crash the program. TBF
#   (TBF - To-Be-Fixed)
#
# * Feel free to add on to this Candela
#
#   CZ
#
#---------------------------------------------------------------#
