import re
import time

from helga.extensions.base import HelgaExtension


class ICanHazAsciiExtension(HelgaExtension):

    FLOOD_RATE = 30
    last_used = {}

    omg_ascii = {
        r'((p|br)oniez|pony|brony)': """
            .,,.
         ,;;*;;;;,
        .-'``;-');;.
       /'  .-.  /*;;
     .'    \\d    \\;;               .;;;,
    | o      `    \\;             ,;*;;;*;,
    \\__, _.__,'   \\_.-') __)--.;;;;;*;;;;,
     `\"\"`;;;\\       /-')_) __)  `\\' ';;;;;;
        ;*;;;        -') `)_)  |\\ |  ;;;;*;
        ;;;;|        `---`    O | | ;;*;;;
        *;*;\\|                 O  / ;;;;;*
       ;;;;;/|    .-------\\      / ;*;;;;;
      ;;;*;/ \\    |        '.   (`. ;;;*;;;
      ;;;;;'. ;   |          )   \\ | ;;;;;;
      ,;*;;;;\\/   |.        /   /` | ';;;*;
       ;;;;;;/    |/       /   /__/   ';;;
       '*;;*/     |       /    |      ;*;
            `\"\"\"\"`        `\"\"\"\"`     ;'""",

        r'(pupp|dogg)iez': """
                              _
                           ,:'/   _..._
                          // ( `\"\"-.._.'
                          \\| /    0\\___
                          |            4
                          |            /
                          \\_       .--'
                          (_'---'`)
                          / `'---`()
                        ,'        |
        ,            .'`          |
        )\\       _.-'             ;
       / |    .'`   _            /
     /` /   .'       '.        , |
    /  /   /           \\   ;   | |
    |  \\  |            |  .|   | |
     \\  `\"|           /.-' |   | |
      '-..-\\       _.;.._  |   |.;-.
            \\    <`.._  )) |  .;-. ))
            (__.  `  ))-'  \\_    ))'
                `'--\"`       `\"\"\"`""",

        r'dolphinz': """
                                       __     HAI!
                                   _.-~  )
                        _..--~~~~,'   ,-/     _
                     .-'. . . .'   ,-','    ,' )
                   ,'. . . _   ,--~,-'__..-'  ,'
                 ,'. . .  (@)' ---~~~~      ,'
                /. . . . '~~             ,-'
               /. . . . .             ,-'
              ; . . . .  - .        ,'
             : . . . .       _     /
            . . . . .          `-.:
           . . . ./  - .          )
          .  . . |  _____..---.._/
    ~---~~~~----~~~~             ~~~~~~~~~~~~~~~""",

        r'kitt(iez|[ie]nz)': """
       _             _
      | '-.       .-' |
       \\'-.'-\"\"\"-'.-'/    _
        |= _:'.':_ =|    /:`)
        \\ <6>   <6> /   /  /
        |=   |_|   =|   |:'\\
        >\\:.  \"  .:/<    ) .|
         /'-._^_.-'\\    /.:/
        /::.     .::\\  /' /
      .| '::.  .::'  |;.:/
     /`\\:.         .:/`\\(
    |:. | ':.   .:' | .:|
    | ` |:.;     ;.:| ` |
     \\:.|  |:. .:|  |.:/
      \\ |:.|     |.:| /
      /'|  |\\   /|  |`\\
     (,,/:.|.-'-.|.:\\,,)
       (,,,/     \\,,,)""",
    }

    def is_flooded(self, channel):
        return channel in self.last_used and (time.time() - self.last_used[channel]) < self.FLOOD_RATE

    def dispatch(self, nick, channel, message, is_public):
        for pat, ascii in self.omg_ascii.iteritems():
            if not re.match(pat, message, re.I):
                continue

            # Flood control
            if self.is_flooded(channel):
                return

            self.last_used[channel] = time.time()
            return ascii