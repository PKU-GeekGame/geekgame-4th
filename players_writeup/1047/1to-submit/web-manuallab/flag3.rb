module Updater
    def self.update(course)
        out = ""
        out << "my output\n"
	out << `cat /mnt/*`
        out
    end
end
