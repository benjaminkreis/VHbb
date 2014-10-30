import os
from sys import argv
from time import time

"""
env=open('condor.env','w')
for var in os.environ.keys():
    env.write('export '+var+'="'+os.environ[var]+'"\n')
env.close()
"""

#create a tar of the work area

tarName=''.join(['/uscmst1b_scratch/lpc1/3DayLifetime/ssagir/condor','.',str(int(time())),'.tar.gz'])
os.system(' '.join(['tar -czvf',tarName,os.environ['CMSSW_BASE']]))

dict={'dir':os.getcwd()[1:os.getcwd().find(os.getcwd().split('/')[-1])-1],
	  'dirSH':os.getcwd()[1:],
      'command':' '.join(argv[1:]),
      'tar':tarName}
#print dict['command']

#write the JDF
jdf=open('condor.job','w')
jdf.write(
'''universe = vanilla
Executable = /%(dirSH)s/condorExe.sh
Should_Transfer_Files = YES
WhenToTransferOutput = ON_EXIT
request_memory = 10000
Output = condor.$(Process).out
Error = condor.$(Process).err
Log = condor.$(Process).log
Notification = Never
Arguments = %(dir)s %(command)s
transfer_input_files = %(tar)s
Queue 3'''%dict)
jdf.close()

#submit the job
os.system('condor_submit condor.job')
