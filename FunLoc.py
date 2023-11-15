#this will be a python version of FunLoc 
from psychopy import visual, core, clock, event, gui
from psychopy.visual.grating import GratingStim
import pandas as pd
import csv
import random
import sys
import os
import numpy as np


def create_img_list(block_order):
    
    faces_dir =  'localizer_images/faces'
    houses_dir = 'localizer_images/houses'
    # objects_dir = 'localizer_images/objects'
    
    # generate the image list: 
    faces = []
    houses = []
    # objects = []

    for ii in range(1, 41):
        faces_path = f"{faces_dir}/{ii}.jpg"
        houses_path = f"{houses_dir}/{ii}.jpg"
        # objects_path = f"{objects_dir}/{ii}.jpg"

        faces.append(faces_path)
        houses.append(houses_path)
        # objects.append(objects_path)
    
    # %create stim_order, with exactly 6 incidental 1-backs
    targets = 0
    while targets != 6:
        stim_order = [list(np.random.choice(range(1, 41), size=20, replace=True)) for _ in block_order]
        targets_temp = [sum(np.diff(order) == 0) for order in stim_order]
        targets = sum(targets_temp)
    # order_list is a list of 12 lists with 20 numbers   
    
    trial_per_block = 20
    image_block=[]
    image_run = []
    for i in range(len(block_order)):
        for ii in range(trial_per_block):
            if block_order[i] ==1:
                image_path=faces[stim_order[i][ii]-1]
            else:
                image_path=houses[stim_order[i][ii]-1]
            image_block.append(image_path)
        image_run.append(image_block)
        image_block=[]
    return image_run

    # order_list is a list of 12 lists with 20 image path   


def run(a,win, out_dir, subj_id, image_run, block_order):

    # wait for fMRI scanner 
    text = visual.TextStim(win, text = 'waiting for scanner', height = 0.05, pos = (0, -0.35), color = "black")
    text.draw()
    win.flip()
    event.waitKeys(keyList = ['5'])
    event.clearEvents()

    #parameters to set before iteration
    global_clock = core.Clock()
    log_block = []
    log_run = np.empty((0,9))
    keyPress = '0'
    # correct = None # if the response is correct
    # keyPress = '0' #if the response has been made or not
    # next_image = None #for image preload buffer
    trial_per_block = 20
    
    run_start= global_clock.getTime()
    for b in range(len(block_order)):
        mask = GratingStim(win, tex=None, mask='circle', size=(0.00587,0.01), color='white')
        mask.draw()
        win.flip()
        while global_clock.getTime()- run_start< 5.0+b*20:
            continue
        # core.wait(15.0) #wait for 15 seconds

        for c in range(trial_per_block):
            startTime= global_clock.getTime()
            trial_num = c+1
            block_num = b+1
            ResponseTime = None
            keys = ()
            img = visual.ImageStim(win, image = image_run[b][c], pos = (0, 0.1))
            img.size = (0.5,1.14)
            img.draw()
            mask.draw()
            win.flip()
            
            #core.wait(0.3)
            while global_clock.getTime()- startTime < 0.30:
                if len(keys) > 0:
                    continue
				# else, if no key_press has been made yet, check for possible response 
                else:
                    keys = event.getKeys(keyList= ['1'])
                    if '1' in keys:  # if 1 is pressed
                        keyPress = '1'
                        ResponseTime = global_clock.getTime() - startTime
                         
            img_dur=global_clock.getTime()- startTime

            mask.draw()
            win.flip()
            while global_clock.getTime()- startTime < 0.75:
                if len(keys) > 0:
                    continue
                else:
                    keys = event.getKeys(keyList= ['1'])
                    if '1' in keys:  # if 1 is pressed
                        keyPress = '1'
                        ResponseTime = global_clock.getTime() - startTime
            trial_dur = global_clock.getTime()- startTime


            log_block.append([block_num,trial_num, image_run[b][c], 
                    startTime, img_dur,trial_dur, global_clock.getTime(), keyPress, ResponseTime
                    ])
            keyPress= '0'
            
        log_run=np.vstack((log_run,log_block))
        log_block = []
    logging_df = pd.DataFrame(log_run, columns = ['block_num','trial_id','ImgPath', 
                                            'onset','img_dur','trial_dur','end_time', 'response',' ResponseTime'
                                            ])

    logging_df.to_csv(out_dir+ f'{subj_id}_run{a+1}.csv' )

    mask.draw()
    win.flip()
    core.wait(30.0) #wait for 15 seconds


if __name__ == "__main__":
    try: 
        subj_id = str(sys.argv[1]) #input the assigned subject numebr in the terminal line
        number_of_runs = int(sys.argv[2])
        out_dir = f"output/{subj_id}/"
        if not os.path.exists (out_dir):
            os.makedirs(out_dir)
        
        win = visual.Window(size=[1920,1080], fullscr=False, color="gray", screen=1) # for Mac,use useRetina=True

    except Exception as e:
        print('Error in retrieving trial selections for %s. Please ensure that trial selections exist and the subjID key is correct' % (subj_id))
        exit()

    # start_input = input('Press y on gui to continue. ')
    event.waitKeys(keyList = ['y']) # halt until y pressed in the test screen (not the terminal)
    event.clearEvents()

    for a in range(number_of_runs):
        print("RUNNING: subject number %s. run number %s" %(subj_id, a+1) )
        if random.choice([1, 2]) == 1:
            block_order = [1, 2]*6
        else:
            block_order = [2, 1]*6
        image_list = create_img_list(block_order)

        run(a,win, out_dir, subj_id, image_list, block_order)




        # # preload stim for next presentation
        # stimTimer = clock.StaticPeriod(screenHz=60)
        # stimTimer.start(0.5)  # start a period of 0.2s
        # if it+1 < 161:
        #     next_image = visual.ImageStim(win, image = img_path + trial_order.face[it + 1], pos = (0, 0.1))
        # stimTimer.complete()
            
            # ResponseTime = None
            # keys = ()
            # # wait here untile the end_time is reached
            # while global_clock.getTime() < row.end_time:
                
            #     # if a key_press has been already made, continue (ignore the later response after initial response)
            #     if len(keys) > 0:
            #         continue
            #     # else, if no key_press has been made yet, check for possible response 
            #     else:
            #         keys = event.getKeys(keyList= ['1'])
            #         if '1' in keys:  # if 1 is pressed
            #             keyPress = '1'
            #             ResponseTime = global_clock.getTime() - startTime
            #             if 1 == row.correct :
            #                 correct = '1'
            #             else :
            #                 correct = '0'
  
    #write output of logging for this run