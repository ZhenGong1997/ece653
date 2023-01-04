# Skeleton repository for STQAM

All code for the course will be distributed through this repository. 

Each student/group also has a personal repository to submit their work. 
The location of student repository is at

  https://git.uwaterloo.ca/stqam-1225/class/<USERID>

where <USERID> is the student gitlab user id (usually the same as Quest user id)

## Initial setup instructions

```
$ git clone https://git.uwaterloo.ca/stqam-1225/class/<USERID> stqam
$ cd stqam
$ git remote add upstream https://git.uwaterloo.ca/stqam-1225/skeleton
$ git fetch upstream
$ git checkout -b master origin/master
$ git merge upstream/master --allow-unrelated-histories
$ git push origin master
```

# Fetch new changes from the skeleton (upstream)

```
$ cd stqam
$ git fetch upstream
$ git merge upstream/master
$ git push origin master
```

# Submit completed assignment

```
$ cd stqam
$ git push origin master
```

Make sure to check that the changes are properly submitted online by following 
https://git.uwaterloo.ca/stqam-1225/class/<USERID> with your web browser.
