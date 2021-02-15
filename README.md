# Introduction
When installing a package on an operating system, several things must be done in a specific order to make the software available to the user, e.g. downloading the package file, extracting it in a temporary locaton, checking for file collisions with already installed packages, moving the files to their final location and optionally executing some post-install code on the system, like adding a user. On Gentoo Linux [1] these steps are Bash [2] code called "phase functions" [3] and since Gentoo Linux compiles software from source code, there are quite a few that you will not find on other OSes.
 
Since compiling software takes a lot of time and modern processors offer multiple cores, anything that can help parallelize the workload is welcomed. On one hand, packages often use build systems that support parallellization, which can speed up the compilation of a single package. On the other hand, the Gentoo Package manager also supports the installation of several packages in parallel, as long as these packages don't depend on each other at build-time.

At first glance, however, the latter does not always seem to yield the expected increased throughput. The goal of this mini-project is to visualize the actions of the Gentoo package manager over time in an attempt to better understand why that is and to see how twiddling with the package manager options, like removing certain not-so-important locks, can improve the situation.

To collect data, we used a nice feature of the package manager where it allows a user to have hooks run before and after each of the phase functions. More specifically, the following code

	for i in pkg_pretend pkg_setup src_unpack src_prepare src_configure src_compile src_test src_install pkg_preinst pkg_postinst
	do
		eval "pre_$i()  { local SANDBOX_WRITE=${SANDBOX_WRITE}; addwrite /var/log/ebuild-timings.txt; echo \$(cat /proc/uptime | cut -d' ' -f1) \${PN}-\${PVR} $i BEGIN >> /var/log/ebuild-timings.txt ; }"
		eval "post_$i() { local SANDBOX_WRITE=${SANDBOX_WRITE}; addwrite /var/log/ebuild-timings.txt; echo \$(cat /proc/uptime | cut -d' ' -f1) \${PN}-\${PVR} $i END >> /var/log/ebuild-timings.txt ; }"
	done

defines additonal pre_* and post_* functions which write timestamps to a log file. 

The task is to write a program that takes such a file as input and produces a schematic on which it is immediately visible which phase function of which package was running when.

# Installation
I recommend installing numpy and pandas, since you will most likely use them.

    $ pip install numpy
    $ pip install pandas
    
Then, just install Dash. Plotly comes with Dash

    $ pip install dash
    
If you'd like to control the version of Plotly installed, you can do for example:

    $ pip install plotly==4.9.0