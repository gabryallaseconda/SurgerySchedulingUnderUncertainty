# Python STL
from abc import ABC, abstractmethod
import math

# Packages
import numpy as np
import pandas as pd # togliere

# Modules
from .predictive_model import PredictiveModel
from .schedule import Schedule
from .task import Task
from ._probability_utils import equiprobability_allocation_from_sampling


class Adversary(ABC): 

    #def __init__(self, predictor:PredictiveModel, schedule:Schedule, task:Task, description = ""):
    def __init__(self, schedule:Schedule, task:Task, description = ""):
        self._description = description
        #self._predictor = predictor
        self._schedule = schedule
        self._task = task
        
    # Getters and setters
    def get_description(self):
        return self._description
    def set_description(self, new:str):
        self._description = new
    description = property(get_description, set_description)

    # def get_predictor(self):
    #     return self._predictor
    # def set_predictor(self, new:PredictiveModel):
    #     self._predictor = new
    # predictor = property(get_predictor, set_predictor)

    def get_schedule(self):
        return self._schedule
    def set_schedule(self, new:Schedule):
        self._schedule = new
    schedule = property(get_schedule, set_schedule)

    def get_task(self):
        return self._task
    def set_task(self, new:Task):
        self._task = new
    task = property(get_task, set_task)

    # Abstract methods
    @abstractmethod
    def run(self):
        pass


class EquiprobableVertex(Adversary):

    #def __init__(self, predictor:PredictiveModel, schedule:Schedule, task:Task, description = ""):
    #    super().__init__(predictor, schedule, task, description)
     
    def __init__(self, schedule:Schedule, task:Task, description = ""):
        super().__init__(schedule, task, description)
     
        
    def run(self):
        
        # robustness_flag variable for correctness. If the risk of overtime is too high, this variable turns false
        # and a new iteration of the I-A is required. Moreover, the times a schedula violates the risk
        # are counted
        robustness_flag = True
        fragile_blocks = 0

        # Run check and the possible generation of a new realization on each block in the schedule
        #for block, info in schedule.items():
        for block in self.schedule._blocks: 
            
            #patients = block.patients

            # Check if in the block there is only one patient: in this case no check sould be performed.
            # TODO: avvisare se la schedula anche con un solo paziente rischia di sforare
            if block.get_num_of_patients() in [0,1] :
                continue

            # Data structures to be filled in the next loop - explanations follows
            samples = []
            samples_ordered = []
            expected_total_duration = 0

            #####################
            # For each single patient, get the sampled data and calculate the sum of nominal values 
            # inside the current block
            
            for patient in block.patients:
                # Use a probabilistic tool to sample from patient duration distribution
                sample = patient.uncertainty_profile.sample(size = 10000)  # TODO mettere nelle impostazioni generali o nel task
                
                # Store the samples of each patient
                samples.append(sample)
                # Store the ordered samples of each patient
                samples_ordered.append(np.sort(sample, axis=-1))
                
                # Store the expected total duration of the current block
                expected_total_duration += patient.uncertainty_profile.nominal_value
                #instance_data[instance_data.patient_num == int(patient)].duration.iloc[
                #    0]  # iloc to get the first value of the series regardless of the index

                # DEBUG
                #if math.isnan(expected_total_duration):  # todo: this was for debug - remove
                #    print(patient)
                #    print(patients)

            #################
            # Evaluation of the overtime in data  associated to the risk
            # Samples are summed to have a sampling of the time of the complete schedule
            # Then the quantile is picked
            # From the instance_config, here is get the risk
            Z_bar = np.quantile(sum(samples), 1 - self._task.robustness_risk)
            #TODO: SALVALRE LA SERIE STORICA DI QUESTI Z_BAR

            # This is where the check on the schedule is performed
            # from the instance_config, here is get the overtime
            
            #if Z_bar >= info.get('block_time') + self._task.robustness_overtime:
            if Z_bar >= block.duration + self.task.robustness_overtime:
            
                # The control is passed only if the schedule does not respect the requirement
                # The robustness_flag turns false
                robustness_flag = False
                fragile_blocks += 1

                # Overtime of maximum risk with respect the expected duration of the block is calculated
                overtime = Z_bar - expected_total_duration

                # Use a probabilistic tool to distribute with equiprobability the overtime
                index = equiprobability_allocation_from_sampling(samples_ordered=samples_ordered,
                                                                robusttime=Z_bar
                                                                )

                # Adding a column to store the realization
                #count_of_realizations = len([x for x in instance_data.columns if x[0:8] == 'epsilon_']) + 1
                #column_this_realization = str('epsilon_' + str(count_of_realizations))
                # instance_data[column_this_realization] = 0.0 # todo cancellare se quello dopo funziona
                #zeros_df = pd.DataFrame(0.0, index=instance_data.index, columns=[column_this_realization])
                #instance_data = pd.concat([instance_data, zeros_df], axis=1)
                
                # create a container for all the adversary realizations
                adversary_realization = {}

                # Now fill the instance_data dataframe with the new realization
                for pat_num, patient in enumerate(block.patients):
                    
                    # Get the index of the patient in the instance_data dataframe
                    #patient_index = instance_data.index[instance_data['patient_num'] == patient].to_list()[0]
                    # Get the extra value of the realization - eps stands for epsilon
                    #eps = max(float(samples_ordered[patients.index(patient)][index]) - instance_data[
                    #    instance_data.patient_num == int(patient)].duration.iloc[0], 0)
                    #if eps < 0:
                    #    raise ValueError("eps cannot be less than 0!")
                    # Place the esp in the column of the realization for the current patient
                    #instance_data.at[patient_index, column_this_realization] = eps
                    
                    adversary_realization.update({
                        patient.id : max(
                            samples_ordered[pat_num][index] - patient.uncertainty_profile.nominal_value,
                            0
                        ) 
                    })
                    
                # Save the adversary realization
                self.task.add_adversary_realization(adversary_realization=adversary_realization)
                                        
                    
                # Vertex realizations
                for patient in block.patients:
                    # Adding a column to store the realization
                    #count_of_realizations = len([x for x in instance_data.columns if x[0:8] == 'epsilon_']) + 1
                    #column_this_realization = str('epsilon_' + str(count_of_realizations))
                    #zeros_df = pd.DataFrame(0.0, index=instance_data.index, columns=[column_this_realization])
                    #instance_data = pd.concat([instance_data, zeros_df], axis=1)

                    # Save a list of the patients in the block excluding the current patient
                    other_patients = [x for x in block.patients if x != patient]

                    # Use a probabilistic tool to sample from patient duration distribution
                    sample = patient.uncertainty_profile.sample(size = 10000) 

                    # Evaluation of the overtime in data associated to the risk
                    # For a single patient
                    # Then the quantile is picked
                    # From the instance_config, here is get the risk
                    H_bar = np.quantile(sample, 1 - self.task.robustness_risk)

                    # Overtime of maximum risk with respect the expected duration of the patient is calculated
                    #patient_overtime = H_bar - instance_data[instance_data.patient_num == int(patient)].duration.iloc[0 ]
                    patient_overtime = H_bar - patient.uncertainty_profile.nominal_value

                    # Different flows if the single patient absorbs all the overtime or not
                    if patient_overtime >= overtime:  # todo check mathematics if this is possible
                        # All the overtime is allocated to the single patient
                        #patient_index = instance_data.index[instance_data['patient_num'] == patient].to_list()[0]
                        # Observe that we allocate the initial overtime, not the patient overtime
                        #instance_data.at[patient_index, column_this_realization] = overtime
                        print("Patient overtime here is greather than overtime!") # TODO rimuovere le cose di debug
                        
                        adversary_realization.update({
                            patient.id : overtime
                        })
                        self.task.add_adversary_realization(adversary_realization=adversary_realization)

                        # TODO: questa cosa non ha senso, non ha senso caricare un solo paziente dell'overtime totale, 
                        # si potrebbe avere la non ammissibilità solo per questo
                    
                    else:
                        overtime_to_allocate = overtime - patient_overtime
                        # A correctness check
                        if overtime_to_allocate <= 0:
                            raise ValueError("Overtime to allocate must be strictly positive in this flow.")
                        
                        adversary_realization = {}
                        
                        # TODO: i due comandi che seguono vanno messi prima della definizione di overtime_to_allocate
                        # Get the index of the patient in the instance_data dataframe
                        #patient_index = instance_data.index[instance_data['patient_num'] == patient].to_list()[0]
                        # Place the patient overtime in the column of the realization for the current patient
                        #instance_data.at[patient_index, column_this_realization] = patient_overtime
                        
                        
                        adversary_realization.update({
                            patient.id : overtime
                        })


                        # Equiprobability allocation for the other patients

                        # Data structure to store the samples
                        samples_ordered_vertex = []
                        # Store the expected duration of the current block excluding the vertex patient
                        expected_partial_duration = 0

                        # Get the ordered samples for each of the other patients
                        for other_patient in other_patients:
                            # Use a probabilistic tool to sample from patient duration distribution
                            sample = other_patient.uncertainty_profile.sample(size = 10000)
                            #sample = patient_duration_sampler(patient_data=patient_data,
                            #                                patient=int(other_patient)
                            #                                )
                            # Store the ordered samples
                            samples_ordered_vertex.append(np.sort(sample, axis=-1))

                            expected_partial_duration += other_patient.uncertainty_profile.nominal_value 
                            #instance_data[instance_data.patient_num == int(other_patient)].duration.iloc[0]

                        # Get the robust-time for this patient (was Z_bar before)
                        robusttime = overtime_to_allocate + expected_partial_duration

                        # Use a probabilistic tool to distribute with equiprobability the overtime
                        index = equiprobability_allocation_from_sampling(samples_ordered=samples_ordered_vertex,
                                                                        robusttime=robusttime
                                                                        )
                        # Fill the other patient esp value
                        for other_pat_num, other_patient in enumerate(other_patients):
                            
                            # Get the index of the patient in the instance_data dataframe
                            #patient_index = instance_data.index[instance_data['patient_num'] == other_patient].to_list()[0]
                            # Get the extra value of the realization - eps stands for epsilon
                            #eps = max(float(samples_ordered_vertex[other_patients.index(other_patient)][index]) - \
                            #    instance_data[instance_data.patient_num == int(other_patient)].duration.iloc[0], 0)
                            # Correctness check
                            #if eps < 0:  # todo check this from a mathematical pov
                            #    raise ValueError("Eps cannot be negative")

                            # Place the esp in the column of the realization for the current patient
                            #instance_data.at[patient_index, column_this_realization] = eps
                            
                            adversary_realization.update({
                                other_patient.id : max(
                                    samples_ordered[other_pat_num][index] - other_patient.uncertainty_profile.nominal_value,
                                    0
                                ) 
                            })
                            
                        self.task.add_adversary_realization(adversary_realization=adversary_realization)


        return robustness_flag, fragile_blocks
    
