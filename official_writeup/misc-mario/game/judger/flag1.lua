local utils = require('utils')

local function main()
  if not utils.load_rom_and_movie() then
    return -1
  end

  utils.run_until_movie_ends()

  local world, level = utils.get_world_level()
  if world == 7 and level == 3 and utils.get_current_page() >= 20 then
    -- Must at the end of level 8-4.
    return 0
  else
    return 1
  end
end

utils.end_emulation(main())
