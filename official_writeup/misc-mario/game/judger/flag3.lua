local utils = require('utils')

local function main()
  if not utils.load_rom_and_movie() or not utils.load_mem_dump() then
    return -1
  end

  utils.run_until_movie_ends()
  return 0
end

utils.end_emulation(main())
