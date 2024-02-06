# [ParameterRandomizer](https://github.com/dustractor/ParameterRandomizer)
---


Randomize parameters of the focused effect or generator plugin. Also provides the ability to copy and paste parameters from one instance of a plugin to another.

## Installation


Clone this repository to

    C:\Users\<username>\Documents\Image-Line\FL Studio\Settings\Hardware


## Setup
Have a midi controller with pads set to the mode to send CC messages.

In FL Studio Midi Settings dialog, select the midi controller in the list of input devices and select this script "ParameterRandomizer" on the controller type option menu.


## Configuring which pads to use

By default the CC messages this script responds to are CC# 20, 21, 22, and 23 but you can edit the file to change this, or you may use the following functions to change the assignment on the fly:
* ``setrandomizerpad(n)``
* ``setrandomizerpad_hex(n)``
* ``setparaminfopad(n)``
* ``setparaminfopad_hex(n)``
* ``setcopypad(n)``
* ``setcopypad_hex(n)``
* ``setpastepad(n)``
* ``setpastepad_hex(n)``

The value for *n* should be quoted for the hex variants.

To find out what CC number your pads send, you may use the Debugging Log (found on FL's options menu), a utility such as MIDI-Ox, or the software provided by the device manufacturer.

To find the value using the Debugging Log, press the desired pad on your controller and the CC value will be shown in hexadecimal in the second numerical column of the output.

Example output:

    ParameterRandomizer:  B0  1A  00  Control Change: 
    Not handled  Absolute 0%

*(In this example, 1A is the the value we are concerned with.)*

If you use the editing software that came with your device, CC values will typically be shown in decimal.

To make this script use that pad during this session, open the Script info window found on FL Studio's View menu (Or use hotkey Ctrl+Alt+S), and on the tab for your device (not the interpreter tab) enter the following:

    setrandomizerpad_hex("1A")

or

    setparaminfopad_hex("1A")
	
depending on which function you want to assign to that pad.

Note the use of quotes since we are supplying a hexadecimal value.  If you know for instance that hexadecimal 1A is 26 in base-10, use one of these functions instead:

    setrandomizerpad(26)

or

    setparaminfo_pad(26)

## Usage

A generator or effect plugin must have the focus. In other words, the last thing you clicked should be the title bar of the plugin you want to randomize the parameters for.

Press the randomizer pad to randomize the parameters.  By default, all available parameters are randomized.

It may not be desirable to randomize certain parameters, such as a dry/wet knob for example. Two utility functions are available in the Script output window for dealing with this: ``lock(<plugin-name>, *<parameter-index>)`` and ``unlock(<parameter-name>, *<parameter-index>)``.

The purpose of the Parameter-info pad is to assist with finding these index numbers.

With the generator or effect plugin focused, press the pad assigned to the Parameter-info function and view the output in the Script output window.

Here is an example using Fruity Flanger. After pressing the Parameter-info pad, the following is shown in the Script output window:

    name: Fruity Flanger
    0 Delay
    1 Depth
    2 Rate
    3 Phase
    4 Damp
    5 Shape
    6 Feed
    7 Invert feedback
    8 Invert wet
    9 Dry
    10 Wet
    11 Cross

If you want to tell the randomizer to ignore the Dry and Wet parameters, you would enter the following in the Script output window:

    lock("Fruity Flanger",9,10)

A list of locked parameters is displayed.

If you later decide to unlock a parameter, such as Wet for example:

    unlock("Fruity Flanger",10)

Multiple indices may be supplied, so if you want to lock or unlock a range of parameters, be sure to prefix the range with an asterisk.  So for example you can first lock all the parameters and then unlock only the ones you want like this:

##### Lock parameters 0-11:
    lock("Fruity Flanger",*range(12))

##### Unlock rate and feedback:
	unlock("Fruity Flanger",2,6)

*(Note the 12 used as the argument to the range function.  The range yields 12 things -- starting with 0 -- so the last value is 11.  If we had said range(11), then the 'cross' parameter would have remained unlocked.)*

**No-name parameters** are parameters that either don't have a name or have a name that starts with "MIDI CC #" or "MIDI Channel ".  They are ignored by default and shown with an asterisk in the parameter info report.  To change this you may use ``ignorenonames(False)``.  It's best to let the randomizer ignore them because having 4000+ automations tends to slow down FL Studio to a standstill.

## Final notes

1. The plugin name shown in the Parameter-info output and supplied to the lock and unlock functions is the plugins "user" name, not the constant plugin name. In other words, if you rename the plugin, the locked parameters will no longer refer to that plugin!

2. Be sure to save your file before using these functions.  Pressing the pads too many times in quick succession can crash the application.
3. For plugins inside of patcher, have the patcher window selected, not the detached window containing the actual plugin.  Also, the parameters must be activated in order to be visible to the script.

