import sys,re
import subprocess
#from splunklib.searchcommands import dispatch, StreamingCommand, Configuration
from splunklib.searchcommands import dispatch, StreamingCommand, Configuration, Option, validators
from splunklib import six

@Configuration()
class jqSearchCommand(StreamingCommand):

    input = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the input field''',
        require=True, validate=validators.Fieldname())
    
    output = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the input field''',
        require=True, validate=validators.Fieldname())
    
    args = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the input field''',
        require=False, validate=validators.Fieldname())
    
    filter = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the input field''',
        require=True)

    split = Option(
        doc='''
        **Syntax:** **fieldname=***<fieldname>*
        **Description:** Name of the input field''',
        require=False)

    def stream(self, records):
        self.logger.debug('jqSearchCommand: %s', self)  # logs command line
        
        for record in records:
            #record['foo'] = 'bar'
            
            command = "jq "+self.args+" "+self.filter
            proc = subprocess.Popen(["jq",self.args,self.filter], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,shell=False,bufsize=2)
            proc_output, errors = proc.communicate(input=record[self.input])
            proc.wait()
            
            if errors != "":
                self.logger.error('jqSearchCommand - errors: %s', errors)  # logs command line
                raise Exception(errors)

            self.logger.debug('jqSearchCommand - output: %s', proc_output)  # logs command line
           
            
            #proc.stdout.close()
            if self.split != "":
                self.logger.debug('jqSearchCommand - split: %s', self.split)  # logs command line
                events = re.split(self.split, proc_output)
                self.logger.debug('jqSearchCommand - split - events: %s', events)
                for i in events:
                    #print(i)
                    if i != "\n":
                        self.logger.debug('jqSearchCommand - split - event: %s', re.sub("\n","",i))
                        record[self.output] = i+self.split
                        yield record
            else:
                record[self.output] = proc_output
                yield record
            

if __name__ == "__main__":
    dispatch(jqSearchCommand, sys.argv, sys.stdin, sys.stdout, __name__)