# ==========================================
#             PROFESSOR-X EDITION
#     Ultra-Speed & Stable Leech Engine
# ==========================================

class _BotCommands:
    def __init__(self):
        self.StartCommand = 'start'
        self.MirrorCommand = ['mirror', 'm']
        self.QbMirrorCommand = ['qbmirror', 'qm']
        self.JdMirrorCommand = ['jdmirror', 'jm']
        self.NzbMirrorCommand = ['nzbmirror', 'nm']
        self.LeechCommand = ['leech', 'l']
        self.QbLeechCommand = ['qbleech', 'ql']
        self.JdLeechCommand = ['jdleech', 'jl']
        self.NzbLeechCommand = ['nzbleech', 'nl']
        self.YtdlCommand = ['ytdl', 'y']
        self.YtdlLeechCommand = ['ytdlleech', 'yl']
        self.CloneCommand = 'clone'
        self.CountCommand = 'count'
        self.DeleteCommand = 'del'
        self.ListCommand = 'list'
        self.SearchCommand = 'search'
        self.StatusCommand = ['status', 's']
        self.UsersCommand = 'users'
        self.AuthorizeCommand = 'authorize'
        self.UnAuthorizeCommand = 'unauthorize'
        self.AddSudoCommand = 'addsudo'
        self.RmSudoCommand = 'rmsudo'
        self.PingCommand = 'ping'
        self.RestartCommand = 'restart'
        self.RestartSessionsCommand = 'restartsession'
        self.StatsCommand = 'stats'
        self.HelpCommand = 'help'
        self.LogCommand = 'log'
        self.ShellCommand = 'shell'
        self.AExecCommand = 'aexec'
        self.ExecCommand = 'exec'
        self.ClearLocalsCommand = 'clearlocals'
        self.BotSetCommand = 'botsetting'
        self.UserSetCommand = 'usetting'
        self.SelectCommand = 'select'
        self.RssCommand = 'rss'
        self.BroadcastCommand = 'broadcast'
        self.ForceStartCommand = ['forcestart', 'fs']
        self.CancelTaskCommand = ['cancel', 'c']
        self.CancelAllCommand = 'cancelall'
        self.IMDBCommand = 'imdb'
        self.MediaInfoCommand = ['mediainfo', 'mi']
        self.NzbSearchCommand = 'nzbsearch'
        self.UpHosterCommand = 'uphoster'
        
        # New Professor-X Features
        self.TTVCommand = 'ttv'

    def refresh_commands(self):
        # This method allows dynamic prefix/suffix updates if implemented later
        pass

BotCommands = _BotCommands()
