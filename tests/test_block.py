import unittest
from surgeryschedulingunderuncertainty.block import Block, MasterBlock#, ScheduleBlock
#from surgeryschedulingunderuncertainty.patient import Patient

class TestBlock(unittest.TestCase):

    def setUp(self):
        self.block = Block(duration=60, equipes=['A', 'B'], weekday=1, order_in_day=1)

    def test_block_getters_setters(self):
        # Costructor
        self.assertEqual(self.block.duration, 60)
        self.assertEqual(self.block.equipes, ['A', 'B'])
        self.assertEqual(self.block.weekday, 1)
        self.assertEqual(self.block.order_in_day, 1)

        # Getters and setters
        self.block.duration = 90
        self.assertEqual(self.block.duration, 90)

        self.block.equipes = ['C', 'D']
        self.assertEqual(self.block.equipes, ['C', 'D'])

        self.block.weekday = 2
        self.assertEqual(self.block.weekday, 2)

        self.block.order_in_day = 2
        self.assertEqual(self.block.order_in_day, 2)

class TestMasterBlock(unittest.TestCase):

    def setUp(self):
        self.master_block = MasterBlock(duration=120, equipes=['A', 'B'], weekday=1, order_in_day=1, order_in_master=1)

    def test_master_block_getters_setters(self):
        # Constructor
        self.assertEqual(self.master_block.duration, 120)
        self.assertEqual(self.master_block.order_in_master, 1)

        # Getters and Setters
        self.master_block.order_in_master = 2
        self.assertEqual(self.master_block.order_in_master, 2)

    # def test_schedule_block(self):  # Patient requires different constructor arguments!
    #     patient1 = Patient(name="John Doe", urgency=3)
    #     patient2 = Patient(name="Jane Doe", urgency=2)

    #     schedule_block = ScheduleBlock(duration=180, equipes=['A', 'B'], weekday=1, order_in_day=1,
    #                                    order_in_week=1, order_in_schedule=1, patients=[patient1, patient2])

    #     self.assertEqual(schedule_block.duration, 180)
    #     self.assertEqual(schedule_block.order_in_week, 1)
    #     self.assertEqual(schedule_block.order_in_schedule, 1)
    #     self.assertEqual(schedule_block.patients, [patient1, patient2])

    #     schedule_block.order_in_week = 2
    #     self.assertEqual(schedule_block.order_in_week, 2)

    #     schedule_block.order_in_schedule = 2
    #     self.assertEqual(schedule_block.order_in_schedule, 2)

    #     patient3 = Patient(name="Bob Smith", urgency=1)
    #     schedule_block.patients.append(patient3)

    #     self.assertEqual(schedule_block.patients, [patient1, patient2, patient3])

if __name__ == '__main__':
    unittest.main()