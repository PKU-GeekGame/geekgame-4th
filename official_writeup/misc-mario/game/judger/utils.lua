local utils = {}

local ROM_FILE = 'Super Mario Bros. (W) [!].nes'
local MOVIE_FILE = 'movie.fm2'
local MEM_DUMP_FILE = 'mem.bin'

--- Loads the ROM file, then pauses the emulator,
--- returns `true` if successful.
---
--- @return boolean
function utils.load_rom()
  local result = emu.loadrom(ROM_FILE)
  if result then emu.pause() end
  return result
end

--- Loads the ROM file and movie file, then pauses the emulator,
--- returns `true` if successful.
---
--- @return boolean
function utils.load_rom_and_movie()
  local result = emu.loadrom(ROM_FILE) and movie.play(MOVIE_FILE)
  if result then emu.pause() end
  return result
end

--- Loads the memory dump file, returns `true` if successful.
---
--- @return boolean
function utils.load_mem_dump()
  local f = io.open(MEM_DUMP_FILE, 'rb')
  if not f then return false end

  local data = f:read('*all')
  if #data ~= 0x800 then return false end

  for i = 1, #data do
    memory.writebyte(i - 1, data:byte(i))
  end
  return true
end

--- Unpauses the emulator and waits until the movie ends.
function utils.run_until_movie_ends()
  emu.unpause()
  while emu.framecount() < movie.length() do
    emu.message('Frame #' .. emu.framecount())
    emu.frameadvance()
  end
end

--- Unpauses the emulator and waits until the movie ends.
--- Calls the given callback function at the end of each frame.
---
--- @param frame_end function
function utils.run_until_movie_ends_with_callback(frame_end)
  emu.unpause()
  while emu.framecount() < movie.length() do
    emu.message('Frame #' .. emu.framecount())
    emu.frameadvance()
    frame_end()
  end
end

--- Saves a screenshot, then terminates the emulator with the given exit code.
---
--- @param exit_code number
function utils.end_emulation(exit_code)
  gui.savescreenshotas('last-frame.png')
  emu.terminate(exit_code)
end

--- Returns Mario's Y position.
---
--- @return number
function utils.get_mario_y_position()
  local hi_pos = memory.readbyte(0xb5)
  local lo_pos = memory.readbyte(0xce)
  return bit.bor(bit.lshift(hi_pos, 8), lo_pos)
end

--- Returns current world and level.
---
--- @return number, number
function utils.get_world_level()
  return memory.readbyte(0x75f), memory.readbyte(0x75c)
end

--- Returns current page.
---
--- @return number
function utils.get_current_page()
  return memory.readbyte(0x725)
end

return utils
