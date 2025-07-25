from textual.app import App
from textual.widgets import Switch,Header,Input,Footer,Label,Button,ProgressBar
from textual.containers import Vertical,Horizontal
from textual.screen import ModalScreen
import argparse
import os
import time
import threading
parser = argparse.ArgumentParser()

parser.add_argument("-f","--file",required=False)

args = parser.parse_args()
filep = args.file


class InfoDialog(ModalScreen):
    def compose(self):
        yield Vertical(
            Label("Incorrect input", id="dialog-label"),
            id="dialog-body"
        )

    def on_mount(self):
        time.sleep(1)
        self.app.pop_screen()
        
class MyApp(App):
    CSS_PATH = "style.tcss"
    CSS = """
    Label{
    height: 3;
    content-align: center middle;
    }
    Horizontal{
    align: left middle
    }
    Input{
    height: 3;
    }
    /* h */
    #h0{
    height: 5;
    width: 100%;
    }
    #h1{
    height: 5;
    width: 100%;
    }
    #h2{
    height: 5;
    width: 100%;
    align: center middle;
    }
    #h3{
    height: 5;
    width: 100%;
    }

    /* File Path */
    #fpl{

    width: 10;
    }
    #fpi{

    width: auto
    }

    /* Offset */
    #ol{

    width: 10;
    }
    #oi{

    width: 20
    }

    /* length */
    #ll{

    width: 10;
    }
    #li{

    width: 20
    }
    /* skip */
    #sl{
    width: 15
    }
    #ss{
    width: auto
    }

    /* btn */
    #spb{
    width: 95%
    }
    """
    ENABLE_COMMAND_PALETTE = False
    def compose(self):
        yield Header()
        yield Vertical(
            Horizontal(
                Label("File Path:",id="fpl"),
                Input(placeholder="File Path",id="fpi"),
                id="h0"
            ),
            Horizontal(
                Label("Offset:",id="ol"),
                Input(placeholder="Offset",id="oi"),
                Label("Length:",id="ll"),
                Input(placeholder="Length(Byte)",id="li"),
                Label("Skip start:",id="sl"),
                #Input(placeholder="Skip Length(Byte)",id="si"),
                Switch("",id="ss"),
                id="h1"
            ),
            Horizontal(
                Button("Start process",id="spb"),
                id="h2"
            ),
            Horizontal(
                Label("",id="il"),
                id="h3"
            )
        )
        
        yield Footer(show_command_palette=False)
    def on_mount(self):
        self.theme = "tokyo-night"
        if filep != None:
            self.query_one("#fpi",Input).value = str(filep)
    def on_button_pressed(self,event:Button.Pressed):
        bid = event.button.id
        il = self.query_one("#il",Label)
        if bid == "spb":
            btn = self.query_one("#spb",Button)
            btn.disabled = True
            il.update("Processing")
            threading.Thread(target=self.process_file).start()
            
    def process_file(self,):
        try:
            try:
                fp = str(self.query_one("#fpi",Input).value)
                offs = int(self.query_one("#oi",Input).value)
                length = int(self.query_one("#li",Input).value)
                skip = bool(self.query_one("#ss",Switch).value)
            except Exception:
                self.call_from_thread(self.set_il,"Incorrect input")
                time.sleep(1)
                self.call_from_thread(self.enable_btn)
                return 
            #self.call_from_thread(self.set_il,bool(skip))
            #raise SystemError
            size = os.path.getsize(fp)
            interval = offs 
            if skip:
                self.call_from_thread(self.set_il,str("skip"))
            else:
                self.call_from_thread(self.set_il,str("noskip"))
            #raise SystemError
            offset = 0
            with open(fp,"r+b") as f:
                while offset + length < size:
                    if offset == 0:
                        if skip:
                            offset += interval
                            continue
                    f.seek(offset)
                    for i in range(length):
                        f.write(b"\x00")
                    offset += interval
                    
            self.call_from_thread(self.set_il,"Completed!")
        except Exception as e:
            #self.call_from_thread(self.set_il,e)
            ...
        self.call_from_thread(self.enable_btn)
    def set_il(self,msg):
        msg = str(msg)
        il = self.query_one("#il",Label)
        il.update(msg)
    def disable_btn(self):
        btn = self.query_one("#spb",Button)
        btn.disabled = True
    def enable_btn(self):
        btn = self.query_one("#spb",Button)
        btn.disabled = False
        


if __name__ == "__main__":
    MyApp().run()
