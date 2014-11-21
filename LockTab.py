import sublime, sublime_plugin

sSettings = sublime.load_settings('LockTab.sublime-settings')

# For ST3
def plugin_loaded():
   global window
   window = sublime.windows()[0]
   global sSettings
   sSettings = sublime.load_settings('LockTab.sublime-settings')

   # Loading lockList and Alert settings
   tempLockList = sSettings.get("locked")
   tempAlert    = sSettings.get("alert")
   tempFocusOCT = sSettings.get("focus_on_closed_tab") 
   # Check that every "locked" file is still in the window
   for tempFile in tempLockList:
      found = False

      for view in window.views():
         if tempFile == view.file_name():
            view.set_status("Locked", "LOCKED")
            found = True
            # and if found, set the locked property

      if not found:
         tempLockList.remove(tempFile) ;

   # saving settings
   sSettings.set("locked", tempLockList)
   sSettings.set("alert", tempAlert)
   sSettings.set("focus_on_closed_tab", tempFocusOCT)
   sublime.save_settings( "LockTab.sublime-settings")

class ToggleTabLockCommand( sublime_plugin.TextCommand ):

   def run(self, edit):

      settings = sublime.load_settings("LockTab.sublime-settings")
      self.Lock_list = sSettings.get("locked")

      if not (self.view.file_name() in self.Lock_list):
         name = self.view.name()
         self.view.set_status("Locked", "LOCKED")

         self.Lock_list.append(self.view.file_name())

      else:
         self.Lock_list.remove(self.view.file_name())
         self.view.erase_status("Locked")

      sSettings.set("locked", self.Lock_list)
      sublime.save_settings( "LockTab.sublime-settings")

   def is_visible(self, paths=None):

      settings    = sublime.load_settings("LockTab.sublime-settings")
      bShowToggle = sSettings.get("show_toggle")
      bHideAll    = sSettings.get("hide_all")

      if (bHideAll):
         return False

      return bShowToggle

class LockTabCommand( sublime_plugin.TextCommand ):   
      
   def run(self, edit):
      ToggleTabLockCommand.run(self, edit)

   def is_visible(self, paths=None):
   # def is_enabled(self, paths=None):
      self.Lock_list = sSettings.get("locked")
      bShowToggle    = sSettings.get("show_toggle")
      bHideAll       = sSettings.get("hide_all")

      if (bHideAll):
         return False

      # Avoiding locking of not-saved file
      if not ( self.view.file_name() ) or bShowToggle:
         return False

      if (self.view.file_name() in self.Lock_list):
         return False

      return True

class UnlockTabCommand( sublime_plugin.TextCommand ):

   def run(self, edit):
      ToggleTabLockCommand.run(self, edit)

   def is_visible(self, paths=None):
   # def is_enabled(self, paths=None):
      self.Lock_list = sSettings.get("locked")
      bShowToggle    = sSettings.get("show_toggle")
      bHideAll       = sSettings.get("hide_all")

      if (bHideAll):
         return False      

      if bShowToggle:
         return False

      if (self.view.file_name() in self.Lock_list):
         return True

      return False

class KeyBindingListener(sublime_plugin.EventListener):

   def on_pre_close(self, view ):

      nId = view.file_name()
      Lock_list = sSettings.get("locked")
      bAlert = sSettings.get("alert")

      if not (nId in Lock_list):
         return

      # Saving tab position
      self.TabPosition = window.get_view_index(view)
      print (str(self.TabPosition[0] ) + str(self.TabPosition[1]) )

      # Saving focus position
      self.visibleRegion = view.visible_region()
      # saving actual active view
      self.ActiveView = window.active_view()

      self.bClose = False;
      # PopUp
      if (bAlert):
         if (sublime.ok_cancel_dialog("Locked Tab. Close it anyway?", "Yes!")):
            self.bClose = True;


   def on_load(self, view):
      # setting focus position
      # if (view.name() in Lock_list):
      view.show(self.visibleRegion.begin())

   def on_close(self, view):

      nId          = view.file_name()
      tempFocusOCT = sSettings.get("focus_on_closed_tab") 
      Lock_list    = sSettings.get("locked")

      # if tab locked
      if (nId in Lock_list):

         # if user confirm closure
         if (self.bClose):
            # removing filename
            Lock_list.remove(nId)
            # exiting
            sublime.save_settings( "LockTab.sublime-settings")
            return

         # if I have to keep the tab opened
         window.run_command("reopen_last_file")

         # setting the old tab position
         vNew = window.active_view()
         window.set_view_index(vNew, self.TabPosition[0], self.TabPosition[1])
         if not tempFocusOCT:
            window.focus_view(self.ActiveView)