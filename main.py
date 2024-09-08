import tkinter as tk
from twitchio.ext import commands
import asyncio
import threading

class TwitchBot(commands.Bot):
    def __init__(self, oauth_token, account_name, bot_name):
        super().__init__(token=oauth_token, prefix='!', initial_channels=[account_name])
        self.bot_name = bot_name

    async def event_ready(self):
        print(f'{self.bot_name} logged in as | {self.nick}')
        print(f'User id is | {self.user_id}')

    async def event_message(self, message):
        if message.author is not None:
            print(f'{message.author.name}: {message.content}')
            await self.handle_commands(message)
        else:
            print('Received a message with no author.')

    @commands.command(name='hello')
    async def hello(self, ctx):
        await ctx.send(f'Hello, {ctx.author.name}!')

    async def send_message(self, channel_name, message):
        channel = self.get_channel(channel_name)
        if channel:
            await channel.send(message)
        else:
            print(f'Channel {channel_name} not found.')

class BotUI:
    def __init__(self, root):
        self.root = root
        root.geometry("850x300")
        self.root.title('Twitch Chat Bot')
        self.create_widgets()

        self.bot = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)

    def create_widgets(self):
        self.account_label = tk.Label(self.root, text="Account Name:")
        self.account_label.grid(row=0, column=0)

        self.account_entry = tk.Entry(self.root)
        self.account_entry.grid(row=0, column=1)

        self.bot_label = tk.Label(self.root, text="Bot Name:")
        self.bot_label.grid(row=0, column=2)

        self.bot_entry = tk.Entry(self.root)
        self.bot_entry.grid(row=0, column=3)

        self.token_label = tk.Label(self.root, text="Auth Token:")
        self.token_label.grid(row=0, column=4)

        self.token_entry = tk.Entry(self.root, show="*")
        self.token_entry.grid(row=0, column=5)

        self.connect_button = tk.Button(self.root, text="Connect", command=self.start_bot)
        self.connect_button.grid(row=0, column=6)

        self.message_label = tk.Label(self.root, text="Message:")
        self.message_label.grid(row=1, column=0)

        self.message_entry = tk.Entry(self.root)
        self.message_entry.grid(row=1, column=1, columnspan=4)

        self.send_button = tk.Button(self.root, text="Send Message", command=self.send_message)
        self.send_button.grid(row=1, column=5)

        self.log_text = tk.Text(self.root, height=10, width=80)
        self.log_text.grid(row=2, columnspan=7)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)

    def start_bot(self):
        account_name = self.account_entry.get()
        bot_name = self.bot_entry.get()
        oauth_token = self.token_entry.get()

        if oauth_token and account_name and bot_name:
            self.bot = TwitchBot(oauth_token, account_name, bot_name)
            self.loop.create_task(self.bot.start())
            self.log(f'Bot {bot_name} connected to account {account_name}.')
            threading.Thread(target=self.loop.run_forever).start()

    def send_message(self):
        if self.bot:
            channel = self.account_entry.get()
            message = self.message_entry.get()
            if self.loop.is_running():
                self.loop.create_task(self.bot.send_message(channel, message))
            else:
                self.log('Event loop is not running.')
            self.log(f'Sent message to {channel}: {message}')
        else:
            self.log('Bot is not connected.')
# Run the application 2
if __name__ == "__main__":
    root = tk.Tk()
    app = BotUI(root)
    root.mainloop()