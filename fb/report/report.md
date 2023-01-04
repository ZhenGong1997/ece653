# REPORT

## Personal Information

- Student Name: Zhen Gong
- Student ID: 20673670
- WatID: z33gong

## What have been done to compile and run the code
I followed the fuzz-battle instructions to compile and run the code: 

1. I installed the docker, connected the container and open on VScode. 
2. Then I git clone and my gitlab fuzz repository and the chocolate-doom repository
3. create a folder named "build" and run cmake command (enable address sanitizer) and ninja command to compile everything
4. disable leak detection to prevent fuzzing stopping when encounter bugs.
5. create folder "CORPUS" under the build folder to collect "interesting" testing inputs.
6. create folder "SEED" under build folder to hold an initial set of inputs for fuzzing. 
7. Run the target in 100 jobs, 10 iterations, and 8 parallel lines.
8. Generate the report on docker, move it to local machine and view in browser

## What have been done to increase the coverage
To increase the coverage, I downloaded several WAD files from the Internet and put them into the SEED folder. The coverage has a remarkable increase because it uses the files in SEED as a template to generate enormous valid inputs and trigger more code paths. At this point, p_setup.c had been covered 82.3% and w_wad.c at more than 70%.

Then I view the coverage report and notice that several edge cases are not covered like :

**w_wad.c: 117-132 (it is looking for filename start with character '~')**

I cover these lines by change the filename in fuzz_target.c from "fuzz.wad" to "~fuzz.wad" and rerun the fuzzing.

**w_wad.c: 143-161 (a comparison between the last three characters of the filename with "wad")**

I cover these lines by changing the filename in fuzz_target.c from "fuzz.wad" to "fuzz.wadas" and rerun the fuzzing.

The coverage of w_wad.c reaches 81.5%. In addition, I tried to increase the total line coverage by adding lines in fuzz_target.c to call methods in i_timer.c and i_sound.c so that the total line coverage reached 10.4%. I stopped here as the work so far should be graded as "Excellent" in the marking schema.

## What bugs have been found? Can you replay the bug with chocolate-doom, not with the fuzz target?
```bash
==69072==ERROR: LeakSanitizer: detected memory leaks

Direct leak of 136 byte(s) in 10 object(s) allocated from:
#0 0x408420 in strdup (/home/doom/stqam/fb/build/src/doom_fuzz+0x408420)
#1 0x4b4e6c in M_StringDuplicate /home/doom/stqam/fb/build/../chocolate-doom/src/m_misc.c:423:14
#2 0x4c8400 in D_BindVariables /home/doom/stqam/fb/build/../chocolate-doom/src/doom/d_main.c:382:26
#3 0x4478b8 in LLVMFuzzerTestOneInput /home/doom/stqam/fb/build/../src/fuzz_target.c:173:3
#4 0x3669e0 in fuzzer::Fuzzer::ExecuteCallback(unsigned char const*, unsigned long) (/home/doom/stqam/fb/build/src/doom_fuzz+0x3669e0)
#5 0x366388 in fuzzer::Fuzzer::RunOne(unsigned char const*, unsigned long, bool, fuzzer::InputInfo*, bool*) (/home/doom/stqam/fb/build/src/doom_fuzz+0x366388)
#6 0x3681a4 in fuzzer::Fuzzer::ReadAndExecuteSeedCorpora(std::__Fuzzer::vector<fuzzer::SizedFile, fuzzer::fuzzer_allocator<fuzzer::SizedFile> >&) (/home/doom/stqam/fb/build/src/doom_fuzz+0x3681a4)
#7 0x3684cc in fuzzer::Fuzzer::Loop(std::__Fuzzer::vector<fuzzer::SizedFile, fuzzer::fuzzer_allocator<fuzzer::SizedFile> >&) (/home/doom/stqam/fb/build/src/doom_fuzz+0x3684cc)
#8 0x35a430 in fuzzer::FuzzerDriver(int*, char***, int (*)(unsigned char const*, unsigned long)) (/home/doom/stqam/fb/build/src/doom_fuzz+0x35a430)
#9 0x37a4b0 in main (/home/doom/stqam/fb/build/src/doom_fuzz+0x37a4b0)
#10 0xffff9781e71c in __libc_start_main (/lib/aarch64-linux-gnu/libc.so.6+0x2071c)
    #11 0x335970 in _start (/home/doom/stqam/fb/build/src/doom_fuzz+0x335970)
```
It detects a lot of memory leaks and above only shows a small portion from the crash-da39a3ee5e6b4b0d3255bfef95601890afd80709 files. This might be caused due to the fuzzing target running on exit (as explained in assignment instructions), and I see them because I didn't turn off the memory-leak flag in the first trail so that it left a record. I did not replay bug with chocolate-doom.
## Did you manage to compile the game and play it on your local machine (Not inside Docker)?
Yes, I uploaded a screenshot of the game as proof.