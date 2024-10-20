local utils = require('utils')

local function main()
  if not utils.load_rom_and_movie() then
    return -1
  end

  utils.run_until_movie_ends()

  local world, _ = utils.get_world_level()
  if world == 35 then
    -- Must at the minus world (world 36).
    return 0
  else
    return 1
  end
end

utils.end_emulation(main())
