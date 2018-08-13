
-- this function is called when the box is initialized
    function initialize(box)
        nRepeat = box:get_setting(2)
        delayTime = box:get_setting(3)
        box:log("Info", string.format("nRepeat: %i", nRepeat))
        box:log("Info", string.format("delayTime: %i", delayTime))
    end
    
    -- this function is called when the box is uninitialized
    function uninitialize(box)
    end
    
    -- this function is called once by the box
    function process(box)
        box:log("Info", "process")
        while box:keep_processing() do
            -- gets current simulated time
            t = box:get_current_time()
            -- loops on all inputs of the box
            for input = 1, box:get_input_count() do
            -- loops on every received stimulation for a given input
                for stimulation = 1, box:get_stimulation_count(input) do
                    -- gets the received stimulation
                    identifier, date, duration = box:get_stimulation(input, 1)
                    -- logs the received stimulation
                    box:log("Trace", string.format("At time %f on input %i got stimulation id:%s date:%s duration:%s", t, input, identifier, date, duration))
                    -- discards it
                    box:remove_stimulation(input, 1)
                    -- triggers a new OVTK_StimulationId_Label_00 stimulation five seconds after
                    for i = 0, nRepeat-1 do
                        box:send_stimulation(1, identifier, t+delayTime+i, 0)
                    end
                end
            end
            -- releases cpu
            box:sleep()
        end     
    end
    
function wait_until(box, time)
    while box:get_current_time() < time do
        box:sleep()
    end
end

function wait_for(box, duration)
    wait_until(box, box:get_current_time() + duration)
end