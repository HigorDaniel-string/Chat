#CHATHD
# passo a passo
# Passo 1: criar botão para iniciar o chat
# Passo 2: Criar um popup para entrar no site
# quando entrar no chat: (aparece para todo mundo)
    # Mostrar mensagem que você entrou no chat
    # o campo e o botão para enviar mensagem
# a cada mensagem que você envia (aparece para todo mundo)
    # Nome: Texto da mensagem

# Passo 1: importar flet
import flet as ft

# Passo 2: definir a função
def main(pagina):
    texto = ft.Text("ChatHD")
    nome_usuario = ft.TextField(label="Escreva seu nome")
    chat = ft.Column()
    

    def enviar_mensagem_tunel(mensagem):
        tipo = mensagem["tipo"]
        if tipo == "mensagem":
            texto_mensagem = mensagem["texto"]
            usuario_mensagem = mensagem["usuario"]
            # adicionar a mensagem no chat
            chat.controls.append(ft.Text(f"{usuario_mensagem}: {texto_mensagem}"))
        else:
            usuario_mensagem = mensagem["usuario"]
            chat.controls.append(ft.Text(f"{usuario_mensagem} entrou no chat", size= 19, italic=True, color=ft.colors.LIGHT_BLUE_900))

        pagina.update()

    # vamos criar o PUBSUB
    pagina.pubsub.subscribe(enviar_mensagem_tunel)


    def enviar_mensagem(evento):
        pagina.pubsub.send_all({"texto":campo_mensagem.value, "usuario": nome_usuario.value, "tipo": "mensagem"})
        # limpar o campo de mensagem
        campo_mensagem.value = ""
        pagina.update()

    campo_mensagem = ft.TextField(label="Digite uma mensagem", on_submit=enviar_mensagem)
    botao_enviar_mensagem = ft.ElevatedButton("Enviar", on_click=enviar_mensagem)

    def entrar_popup(evento):
        pagina.pubsub.send_all({"usuario": nome_usuario.value, "tipo": "entrada"})
        #adicionar o chat
        pagina.add(chat)
        #primeiro vai ter que fechar o popup
        popup.open = False
        
        #remover o botão de iniciar site
        pagina.remove(botao_iniciar)
        pagina.remove(texto)
        #criar o campo de mensagem criar o botão de enviar mensagem
        pagina.add(ft.Row(
            [campo_mensagem, botao_enviar_mensagem]
            ))
        pagina.update()

    popup = ft.AlertDialog(
        open=False, 
        modal=True,
        title=ft.Text("Bem vindo ao ChatHD"),
        content=nome_usuario,
        actions=[ft.ElevatedButton("Entrar", on_click=entrar_popup)],
    )

    def entrar_chat(evento):
        pagina.dialog = popup
        popup.open = True

        pagina.update()

    botao_iniciar = ft.ElevatedButton("Iniciar chat", on_click=entrar_chat)

    pagina.add(texto)
    pagina.add(botao_iniciar)


# Passo 3: iniciar o flet
ft.app(target=main, view=ft.WEB_BROWSER, port=8000)