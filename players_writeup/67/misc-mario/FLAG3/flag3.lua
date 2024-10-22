--- Loads the memory dump file, returns `true` if successful.
---
--- @return boolean
function load_mem_dump()
    local f = io.open("./RAM.dump", 'rb')
    if not f then return false end
  
    local data = f:read('*all')
    if #data ~= 0x800 then return false end
  
    for i = 1, #data do
      memory.writebyte(i - 1, data:byte(i))
    end
    return true
  end

--- Loads the ROM file and movie file, then pauses the emulator,
--- returns `true` if successful.
---
--- @return boolean
function load_rom_and_movie()
    local result = emu.loadrom("../Super Mario Bros. (W) [!].nes") and movie.play("./TAS.fm2")
    if result then emu.pause() end
    return result
  end

load_rom_and_movie()
load_mem_dump()