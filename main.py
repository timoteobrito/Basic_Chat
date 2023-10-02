#STEPS
# 1 - Start chat button
# 2 - Show pop up to enter chat
# 3 - Once in chat:                         *(shows to all chat participants)
        # a) Show message that user is in chat
        # b) Show field and button to send message
# 4 - To every sent message:                *(shows to all chat participants)
        # a) Show "Name: " + <sent_message>

import flet as ft

def main( page ):
    text = ft.Text("HASHZAP\n\n")                       #App main page header
    user_name_field = ft.TextField(label="Name")        #Field to collect username
    chat = ft.Column()                                  #Column to host chat history


    #This function contains what is going to be executed once the PUBSUB is used
    def send_message_tunnel(message):
        log_user = message["user"]

        if message["type"] == "message":        #Block for messages
            log_text = message["text"]            
            chat.controls.append(ft.Text( f"{log_user}: {log_text}" ))
        
        else:                                   #Block for chat entrance
            chat.controls.append(ft.Text( f"{log_user} entered chat", size=12, italic=True, color=ft.colors.ORANGE_500))

        page.update()

    
    page.pubsub.subscribe(send_message_tunnel)      #Subscribes to PUBSUB


    def send_message(event):
        page.pubsub.send_all( { "text": message_field.value, "user": user_name_field.value, "type": "message" } )       #Uses PUBSUB passing a dictionary as argument
        message_field.value = ""
        page.update()


    message_field = ft.TextField(label="Message")
    send_message_button = ft.ElevatedButton("Send", on_click=send_message)
        

    def enter_popup(event):
        page.pubsub.send_all( { "user": user_name_field.value, "type": "entrance" } )       #Uses PUBSUB passing a dictionary as argument
        page.add(chat)
        popup.open=False                                                                    #Removes popup from screen          
        page.remove(chat_start_button)                                                      #Removes button
        page.add( ft.Row( [ message_field, send_message_button ] ) )                        #Adds a Row with a list of items in it
        page.update()
        
    
    #Defines popup object
    popup = ft.AlertDialog(
        open=False,
        modal=True, 
        title=ft.Text("Welcome to Hashzap!!!"),
        content=user_name_field,
        actions=[ft.ElevatedButton("Enter", on_click=enter_popup)]      #Defines popup actions
    )


    def enter_chat(event):
        page.dialog = popup         #Uses popup
        popup.open = True           #Shows popup
        page.update()


    chat_start_button = ft.ElevatedButton( "Start chat", on_click=enter_chat )      #Defines button


    page.add( text )                        #Adds page Header
    page.add( chat_start_button )           #Adds button
    

#######################################################################################################


ft.app( target=main, view=ft.WEB_BROWSER, port=8000 )       #Starts web-based app
#ft.app( target=main )                                       #Starts local python app
