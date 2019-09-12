import os, subprocess, shutil, tempfile
# def twoSum(self, nums: List[int], target: int) -> List[int]:

# class holds properties about the student's grade, and easily print stuff
class Grade:
    def __init__(self):
        pass
    # creates personalized string for each student communicating grade & reason
    def __print__(self): 
        pass

    def invalid(self):
        pass
    def dnc(self):
        pass
    def blank(self):
        pass
    def warnings(self):
        pass

class Grader:
    # pass a string representing the lab name
    def __init__(self, lab: str, files: set, folder='/home/gabe/code/cpsc1111-005/assignments', grading_folder='/home/gabe/code/cpsc1111-005/grading'):
        self.lab = os.path.join(folder, lab)
        self.grade_dir = os.path.join(grading_folder, lab)
        self.files = files
        self.grades = None
        self.tmp_dir = None

    def getFiles(self) -> list:
        for kid in [i.path for i in os.scandir(self.lab) if i.is_dir()]:
            uname = kid.split(os.sep)[-1]
            # if the file is not a mercurial file, return it
            yield [i.path for i in os.scandir(kid) if i.name[-3:]!='.hg'], uname
    
    # str in {'none', 'dnc', 'warn'}
    #   'dnc'  submission does not compile (automatically fails all test cases)
    #   'none' compiles without warnings or errors
    #   'warn' submission compiles with warnings
    def compile(self, f: str, compiler='gcc', flags='-Wall', lib='-lm') -> str:
        # tells gcc where to place binary/executible (tmp dir)
        out = '-o '+self.tmp_dir+'/a.out'
        
        # print(compiler+' '+flags+' '+out+' '+f+' '+lib)
        # print(self.tmp_dir)
        # print([i.path for i in os.scandir(self.tmp_dir)])

        # Note: gcc exit code 1 -> Error in compilation
        #       gcc exit code 0 -> Successful compilation (but could have warning)
        run = subprocess.run([compiler, flags, out, f, lib], 
            universal_newlines=True, stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE)
        print(run.stdout)
        print(run.stderr)
        print(run.returncode)
        # cp.stdout
        # # total 20K
        # # drwxrwxr-x  3 felipe felipe 4,0K Nov  4 15:28 .
        # # drwxrwxr-x 39 felipe felipe 4,0K Nov  3 18:31 ..
        # # drwxrwxr-x  2 felipe felipe 4,0K Nov  3 19:32 .ipynb_checkpoints
        # # -rw-rw-r--  1 felipe felipe 5,5K Nov  4 15:28 main.ipynb
        # cp.stderr
        # # '' (empty string)
        # cp.returncode
        # # 0

    # processes output and grades student on the compilation of their submission
    #   returns False if we should no longer process this student's submission 
    #       (it did not compile)
    #   returns True if we should continue to process submission
    def grade_compile(self, out: str, uname: str) -> bool:
        if out == 'dnc': 
            self.grades[uname].dnc()
            return False
        if out == 'warn':
            self.grades[uname].warnings()
        return True

    def clear_dir(self, directory: str) -> None:
        for root, dirs, files in os.walk(directory):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    # testing on testcases
    # returns the number of passed test cases
    def test(self, bin: str)-> int : 
        pass

    # grading
    # performs grading and prints a chart, grading for each student
    # give input and compare to expected output
    def grade(self) -> None:
        
        # create tmp dir
        self.tmp_dir = tempfile.mkdtemp()

        # create map to store grade & comments
        self.grades = {}

        # grab student submissions and process it
        for f, uname in self.getFiles():
            # TODO remove testing line
            if f != ['/home/gabe/code/cpsc1111-005/assignments/Lab2/ariese/lab2.c']: continue

            self.grade_student(f, uname)

        # clean tmp dir
        # self.clear_dir(self.tmp_dir)
        # shutil.rmtree(self.tmp_dir)

    def grade_student(self, f: str, uname: str) -> None:
        # initalize student's grade object
        self.grades[uname] = Grade()

        # check if student submission is blank
        if not len(f): 
            self.grades[uname].blank()
            return

        # only process the first file for now
        f = f[0]

        # check if student submission matches proper file name
        if not f in self.files: self.grades[uname].invalid()

        # copy files(s) to tmp dir
        shutil.copyfile(f, os.path.join(self.tmp_dir, f.split(os.sep)[-1]))

        # update f to be pointing to the copy of f in the temp. directory
        f = [i.path for i in os.scandir(self.tmp_dir)][0]

        # check if student submission compiles and/or has warnings
        if not self.grade_compile(self.compile(f), uname): return

        # check if student submission passess test cases
        self.test(f)        

subprocess.run(['ls'])

g = Grader(lab='Lab2', files={})
g.grade()