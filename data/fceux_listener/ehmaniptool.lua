local ehhelper = require("ehhelper")
local fceuxlistener = require("fceuxlistener")

function main()
    while true do
        fceuxlistener.update()
        emu.frameadvance()
        ehhelper.update_boxes()
    end
end

gui.register(fceuxlistener.update) --undocumented. this function will call even if emulator paused

main()
