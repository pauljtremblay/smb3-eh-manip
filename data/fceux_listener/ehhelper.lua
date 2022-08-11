-----------------------------------------------------------------------
-- Lua script for displaying "countdown" boxes to assist with
-- jumping on the required frame to achieve EarlyHammer
--
-- Created By: narfman0+orangeexpo+lui
-- For use with the TAS "orange-nodeath-eh-v0.7"
--
-- notes
--
-- 1-1: 87 lag, 290 ingame clock, 3447,3431 end of level lag frame, bro (right, left)
-- 1-2: 164 lag, 293/2 ingame clock, 4950,4935 end of level lag frame, bro (right, left)
-- 1-f: 259 lag, 290 ingame clock, 6426,6411 end of level lag frame, bro (right, left)
-- 1-5: 351 lag, 287 ingame clock, 8442,8406 end of level lag frame, bro (right, left)
-- 1-6: 424 lag, 291 ingame clock, 9914,9875 end of level lag frame, bro (left)
-- 1-bro: 497 lag, 195 ingame clock, 10638,10560 end of level lag frame, FIRE FLOWER
-- 1-koopa: 598 lag, 245 ingame clock, 15655,15563 end of level lag frame
--      orig        a-press on 1-castle 11 frames earlier
--      14214  11   14203 going down pipe
--      14475  14   14461 $0524==A0 frame
--      14631  14   14617 first lift frame of shell flying away
--      14692  14   14678 wand on screen
--      14731  14   14717 wand blue bg frame
--                  15518 last wand frame on screen
--                  15827 wand in kings hand
--                  16686 letter A press, 16687 lag frame
-----------------------------------------------------------------------

local ehhelper = { _version = "0.7" }

local countdown_delay = 24

local goodmeme = 16000
                            --       18433 18434 18435 18436
                            -- 2-1: [good, bad, good*, good]
                            -- bad = MB: left, down
local goodframe_2_1 = 18046 -- 684 lag, 289 ingame clock, 18435 end of level lag frame
                            --18043 jump| 18432-18443 bad (left,up)
                            --18044 jump| 18433-18444 good (right,up)
                            --18045 jump| 18434-18445 bad (left,down)
                            --18046 jump| 18435-18446 good (right,up)
                            --18047 jump| 18436-18447 good (right,up)
                            --18048 jump| 18437-18448 bad (right,down)

                            -- 2-2: [good, good*, good]
local goodframe_2_2 = 19947 -- 769 lag, 285 ingame clock, 20430 end of level lag frame
                            --19945 jump| 20428-20440 bad (down/up)
                            --19946 jump| 20429-20441 good (left,right/up)
                            --19947 jump| 20430-20442 good* (left,right/up)
                            --19948 jump| 20431-20443 good (left,right/up)
                            --19949 jump| 20432-20444 bad (left,right/down)
                            --19950 jump| 20433-20445 bad (down,down/down)

                            -- 2-f: [good, bad*, good]
local goodframe_2_f = 22670 -- 869 lag, 277 ingame clock, 23076 end of level lag frame
-- lag: 845, 856 (pipe 21796-21806), 869 (door 22309-22321)
                            --22665 jump| 23072-23083 bad
                            --22666 jump| 23073-23084 bad (mb: down,down/h: down)
                            --22667 jump| 23074-23085 bad (mb: down,down/h: left,left)
                            --22668 jump| 23075-23086 bad
                            --22669 jump| 23076-23087 good
                            --22670 jump| 23077-23088 bad
                            --22671 jump| 23078-23089 good
                            --22672 jump| 23079-23090 bad
local goodframe_ph  = 23952 -- 940 lag, 24276 end of level lag frame

local screen_width  = 0x10 --256 pixels, 16 blocks
local screen_height = 0x0F --240 pixels, 15 blocks

local nboxes = 11
local floorhalf = math.floor(nboxes/2)
local box_size = 17
local space_size = 5
local box_y = 20
local box2_y = 60
local box2_x = 146

local box_colors = {}

function init_box_colors()
    for i=1, nboxes, 1 do
        box_colors[i] = "#ffffff80"
    end
end

function display_boxes()
    local x_mid = ((screen_width*16)/2) + 8
    local box1_x = x_mid - (box_size*0.5) - ((box_size+space_size)*floorhalf)
    for i=0, nboxes-1, 1 do
        local x = box1_x+(i*(box_size+space_size))
        local b = {x, box_y, x + box_size, box_y + box_size, box_colors[i+1], "white"}
        gui.drawrect(unpack(b))
    end
end

function update_box_colors(frame, curr)
    -- Turn the middle box green on 'frame'
    -- First and last boxes are paired, and so on until the middle one
    -- Threshold for the first box is 'frame' - (floorhalf*countdown_delay)
    if curr < (frame - (floorhalf*countdown_delay) - 30) or curr > (frame + 180) then
        init_box_colors()
        return false
    end
    for i=1, floorhalf+1, 1 do
        if curr >= (frame - ((floorhalf-(i-1))*countdown_delay)) then
            box_colors[i] = "purple"
            box_colors[nboxes-(i-1)] = "purple"
        end
    end
    local b1 = {box2_x, box2_y, box2_x + box_size, box2_y + box_size, "#ffffff00", "white"}
    gui.drawrect(unpack(b1))
    gui.drawline(box2_x - countdown_delay, box2_y, box2_x - countdown_delay, box2_y + box_size)
    gui.drawline(box2_x - countdown_delay*2, box2_y, box2_x - countdown_delay*2, box2_y + box_size)
    gui.drawline(box2_x - countdown_delay*3, box2_y, box2_x - countdown_delay*3, box2_y + box_size)
    gui.drawline(box2_x - countdown_delay*4, box2_y, box2_x - countdown_delay*4, box2_y + box_size)
    local x = box2_x - box_size - (frame - curr)
    if (x+box_size) < 256 then
        local color = "#ffffff80"
        if curr == frame then
            color = "purple"
        end
        local b2 = {x, box2_y, x + box_size, box2_y + box_size, color, "white"}
        gui.drawrect(unpack(b2))
    end
    return true
end

function ehhelper.update_boxes()
    curr = emu.framecount()
	if update_box_colors(goodmeme, curr) then
        -- do nothing
    elseif update_box_colors(goodframe_2_1, curr) then
        -- do nothing
    elseif update_box_colors(goodframe_2_2, curr) then
        -- do nothing
    elseif update_box_colors(goodframe_2_f, curr) then
        -- do nothing
    elseif update_box_colors(goodframe_ph, curr) then
        -- do nothing
    end

    display_boxes()
end

init_box_colors()

return ehhelper