import hl7,random,datetime, string
import hl7.client

class AbstractMessageFactory(object):
    #TODO: Finish returns
    @classmethod
    def factory(cls,id,message_type,version,dataset):
        cls.id = id
        cls.message_type = message_type
        cls.version = version

        #Return correct message based upon version and type
        if cls.version == "2.3":
            if message_type =="SIU_S12":
                return S12_23(id,dataset)
            elif message_type == "SIU_S13":
                return S13_23(id,dataset)
            elif message_type == "SIU_S14":
                return S14_23(id,dataset)
            elif message_type == "SIU_S15":
                return S15_23(id,dataset)
            elif message_type == "SIU_S26":
                return S26_23(id,dataset)
            elif message_type == "Error":
                return ErrorMsg(id, dataset)
            else:
                raise Exception
        else:
            raise NotImplementedError

            
class BaseMessage(object):
    def __init__(self, id, dataset):
        self.id = id
        self.sending_time = datetime.datetime.now().strftime('%Y%m%d%H%M')
        
    def send(self, hostname, port):
        self.client = hl7.client.MLLPClient(hostname, port)
        self.client.send_message(self.message)
        self.client.close()
        
    def save(self, directory):
        #TODO
        pass


class SIU(BaseMessage):
    def __init__(self,id,dataset):
        super(SIU, self).__init__(id, dataset)
        
        #Schedule fields
        self.appointment_time = datetime.datetime.now() + datetime.timedelta(
                                days=random.randint(1,100),
                                minutes=random.randint(0,60),
                                seconds=random.randint(0,60))
        self.appointment_time = self.appointment_time.strftime('%Y%m%d%H%M')
        self.appointment_duration = random.randint(10,180)
        
        #Patient fields
        self.ext_patient_id = random.randint(1,1000000)
        self.int_patient_id = random.randint(1,1000000)
        self.patient_name_last = random.choice(dataset['last_names'])
        self.patient_name_first = random.choice(dataset['first_names'])
        self.mothers_maiden = random.choice(dataset['last_names'])
        self.patient_dob = datetime.datetime(random.randint(1950,2000),
                            random.randint(1,12), random.randint(1,28))
        self.patient_dob = self.patient_dob.strftime('%Y%m%d')
        self.patient_sex = random.choice(['M','F','O','U'])
        self.patient_race = random.choice(dataset['race_codes'])
        self.patient_street = ' '.join([str(random.randint(0,20000)), 
                                random.choice(dataset['street_names']),
                                random.choice(dataset['street_types'])])
        self.patient_city = random.choice(dataset['cities'])
        self.patient_zip = random.randint(10000,99999)
        self.patient_phone = '(%s)%s-%s)' % (random.randint(100,999),
                                             random.randint(100,999),
                                             random.randint(1000,9999))
        self.patient_marital = random.choice(['A','D','M','S','W'])
        self.patient_ssn = '%s-%s-%s' % (random.randint(100,999),
                                         random.randint(10,99),
                                         random.randint(1000,9999))
        
        #Resource fields
        self.set_id = random.randint(1,1000)
        self.resource_id = random.choice(dataset['resource_codes'])
        self.location_id = random.choice(dataset['location_codes'])
        self.personnel_id = random.choice(dataset['personnel_codes'])

        #Define message parts
        self.msh = 'MSH|^~&\|||||%s||SIU^S12|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)
        self.sch = 'SCH|%s||||||||%s|MIN|%s|%s^%s^%s|||||||||||||C|\r' % (
                    random.randint(1,1000), 
                    self.appointment_duration,
                    self.appointment_time,
                    ''.join(random.choice(string.ascii_uppercase) for x in range(6)),
                    random.choice(dataset['last_names']),
                    random.choice(dataset['first_names']))
        self.pid =  'PID|%s|%s|%s||%s^%s|%s|%s|%s||%s|%s^^%s^%s||%s|EN|%s|||%s|||||||||||\r' % (
                    self.id,
                    self.ext_patient_id,
                    self.int_patient_id,
                    self.patient_name_last,
                    self.patient_name_first,
                    self.mothers_maiden,
                    self.patient_dob,
                    self.patient_sex,
                    self.patient_race,
                    self.patient_street,
                    self.patient_city,
                    self.patient_zip,
                    self.patient_phone,
                    self.patient_marital,
                    self.patient_ssn)
        self.rgs = 'RGS|%s|ASDF\r' % self.set_id
        self.ais = 'AIS|%s|||%s|||%s|MIN||C|\r' % (
                    self.set_id,
                    self.appointment_time,
                    self.appointment_duration)
        self.aig = 'AIG|%s||%s|||||%s|||%s|MIN|||\r' % (
                    self.set_id,
                    self.resource_id,
                    self.appointment_time,
                    self.appointment_duration)
        self.ail = 'AIL|%s||%s|||%s|||%s|MIN|||\r' % (
                    self.set_id,
                    self.location_id,
                    self.appointment_time,
                    self.appointment_duration)
        self.aip = 'AIP|%s||%s||||%s|||%s|MIN||\r' % (
                    self.set_id,
                    self.personnel_id,
                    self.appointment_time,
                    self.appointment_duration)
    
    def assemble(self):
        #Generate full message
        self.message = (self.msh + 
                        self.sch +
                        self.pid +
                        self.rgs +
                        self.ais +
                        self.aig +
                        self.ail +
                        self.aip)    

                        
class S12_23(SIU):
    def __init__(self, id, dataset):
        super(S12_23, self).__init__(id, dataset)
        
        self.msh = 'MSH|^~&\|||||%s||SIU^S12|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)

        
class S13_23(SIU):
    def __init__(self, id, dataset):
        super(S13_23, self).__init__(id, dataset)
        
        self.msh = 'MSH|^~&\|||||%s||SIU^S13|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)

        
class S14_23(SIU):
    def __init__(self, id, dataset):
        super(S14_23, self).__init__(id, dataset)
        
        self.msh = 'MSH|^~&\|||||%s||SIU^S14|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)


class S15_23(SIU):
    def __init__(self, id, dataset):
        super(S15_23, self).__init__(id, dataset)
        
        self.msh = 'MSH|^~&\|||||%s||SIU^S15|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)
   

class S26_23(SIU):
    def __init__(self, id, dataset):
        super(S26_23, self).__init__(id, dataset)
        
        self.msh = 'MSH|^~&\|||||%s||SIU^S26|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)


class ErrorMsg(SIU):
    def __init__(self, id, dataset):
        super(ErrorMsg, self).__init__(id, dataset)
        
        #Define MSH, but override the SCH segment to create an error
        self.msh = 'MSH|^~&\|||||%s||SIU^S26|%s|P|2.3||||||\r' % (
                    self.sending_time, self.id)
        self.sch = ''
