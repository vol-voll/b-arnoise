from Main2 import*
from tkinter import*
import tkinter.ttk as ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from pprint import pprint

class fenetre(Tk): 
    def __init__(self):
        Tk.__init__(self) 
        self.title("b-arnoise en fonction")
        self.menuBar()
        self.geometry('520x300')
        self.resizable(1,0)
        self.client_id,self.client_secret,self.redirect_uri, self.contenuPlaylist = "", "", "", []

    def menuBar(self):
        menu_bar = Menu(self)
        menu_deroulant = Menu(menu_bar, tearoff=0)
        menu_deroulant.add_command(label="Importer une playlist", command=self.importPlaylist)
        menu_deroulant.add_command(label="Sauvegarder le travail", command=self.sauver)
        menu_deroulant.add_command(label="Reprendre un travail", command=self.importer)
        menu_deroulant.add_command(label="Rentrer les clés", command=self.setPrivateKey)
        menu_deroulant.add_separator()
        menu_deroulant.add_command(label="Quitter", command=self.quit)
        menu_bar.add_cascade(label = 'Fichier', menu = menu_deroulant)
        self.config(menu=menu_bar)

    def importPlaylist(self):
        self.zoneImport = Frame(self)
        self.zoneImport.grid(row = 0, column = 0)
        self.Type = ttk.Combobox(self.zoneImport, values=["Album", "Playlist"], width=8)
        self.Type.grid(padx=10, pady=5, column=0, row=0)
        self.ecrireURI = ttk.Entry(self.zoneImport, width=28)
        self.ecrireURI.grid(padx=5, pady=5, column=1, row=0)
        self.jeValide = ttk.Button(self.zoneImport, text='Valider', command=self.valider)
        self.jeValide.grid(padx=10, pady=5, column=2, row=0)
        
    
    def valider(self):
        self.Type = self.Type.get()
        self.URI = self.ecrireURI.get()
        self.zoneImport.destroy()
        self.contenuPlaylist=self.chargerPlaylist()
        self.LancerTableauDesChansons()

    def chargerPlaylist(self):
        contenu=[]
        try :
            Key = lire_fichier("PrivateKey")            
            self.client_id,self.client_secret,self.redirect_uri = Key[0],Key[1],Key[2]
        except :
            self.setPrivateKey()
        sp = Spotify_magic(auth_manager=SpotifyOAuth(self.client_id,self.client_secret,self.redirect_uri,scope="user-library-read"))
        
        decalage = 0
        api_call = {'items' : []}
        if self.Type=="Playlist":
            while len(api_call['items']) == 100 or decalage == 0:
                NomPlaylist = sp.user_playlist(user=None, playlist_id=self.URI, fields="name")["name"]
                api_call = sp.playlist_tracks(f"spotify:playlist:{self.URI}", limit=100, offset=decalage)
                for element in api_call['items']:
                    contenu.append(Chanson(element["track"]["name"], element["track"]["artists"], element["track"]["album"]['name'], element["track"]["duration_ms"], element['track']['album']['images'][0]['url'], element['track']['id'], NomPlaylist))
                decalage += 100
        if self.Type=="Album":
            api_call = sp.album(f"spotify:album:{self.URI}")
            NomAlbum = api_call['name']
            Pochette = api_call["images"][0]['url']
            for element in api_call['tracks']['items']:
                contenu.append(Chanson(element["name"], element["artists"], NomAlbum, element["duration_ms"], Pochette, element['id'], NomAlbum))
        return contenu
    
    def setPrivateKey(self):
        self.fenID = Tk()
        self.fenID.resizable(0,0)
        Label(self.fenID, text="Client ID").grid(row=0, column=0, padx=5, pady=2.5)
        Label(self.fenID, text="Client secret").grid(row=0, column=1, padx=5, pady=2.5)
        Label(self.fenID, text="Redirect URI").grid(row=0, column=2, padx=5, pady=2.5)
        self.boutonSpecial = ttk.Button(self.fenID, text = "G 1 Fichier", command=self.FichierDispo)
        self.Entrerclient_id = Entry(self.fenID, width=33, text=self.client_id)
        self.Entrerclient_secret = Entry(self.fenID, width=33, text=self.client_secret)
        self.Entrerredirect_uri = Entry(self.fenID, width=20, text=self.redirect_uri)
        self.jeValide2 = ttk.Button(self.fenID, text='Valider', command=self.valider2)

        self.Entrerclient_id.grid(row=1, column=0)
        self.Entrerclient_secret.grid(row=1, column=1)
        self.Entrerredirect_uri.grid(row=1, column=2)
        self.jeValide2.grid(row=1, column=3)

    def FichierDispo(self):
        self.fenID.destroy()
        Key = lire_fichier(askopenfilename())            
        self.client_id,self.client_secret,self.redirect_uri = Key[0],Key[1],Key[2]

    def valider2(self):
        if len(self.Entrerclient_id.get()) != 32 or len(self.Entrerclient_secret.get()) != 32: #? Pas ce qu'on veut quoi
            self.Entrerclient_id.config(bg="#ff5b5b")
            self.Entrerclient_secret.config(bg="#ff5b5b")
        else :
            self.client_id = self.Entrerclient_id.get()
            self.client_secret = self.Entrerclient_secret.get()
            self.redirect_uri = self.Entrerredirect_uri.get()
            from os import rename, path
            if path.exists("PrivateKey"):
                try :
                    rename("PrivateKey", "PrivateKey.bak")
                except:
                    print("Erreur lors de la création du fichier \"PrivateKey\".")
                    return
            ecrire_fichier(".", "PrivateKey", f"{self.client_id}\n{self.client_secret}\n{self.redirect_uri}\n{logo}")
            self.fenID.destroy()
        
    def LancerTableauDesChansons(self):
        self.BoutonRechercheYt = ttk.Button(self, text='Chercher vidéos YT', command=self.chercherYT) 
        self.BoutonModifierLien = ttk.Button(self, text='Modifier un lien YT', command=self.modifier)
        self.BoutonTéléchargerUn = ttk.Button(self, text='Télécharger une sélection', command=self.telechargerSelection)
        self.BoutonToutTélécharger = ttk.Button(self, text='Tout télécharger', command=self.toutTélécharger)
        self.BoutonRechercheYt.grid(row=0, column=0, padx=5, pady=2)
        self.BoutonModifierLien.grid(row=0, column=1, padx=5, pady=2)
        self.BoutonTéléchargerUn.grid(row=0, column=2, padx=5, pady=2)
        self.BoutonToutTélécharger.grid(row=0, column=3, padx=5, pady=2)

        self.TableauChansons = ttk.Treeview(self, columns=("Titre","Artistes", "Album", 'Durée', "URI de Piste", "VidéoYT", "LienYT"), height=12, show='headings')
        self.geometry('1120x300')
        self.TableauChansons.column("Titre", width=200, anchor='center'); self.TableauChansons.heading("Titre", text="Titre")
        self.TableauChansons.column("Artistes", width=150, anchor='center'); self.TableauChansons.heading("Artistes", text="Artistes")
        self.TableauChansons.column("Album", width=150, anchor='center'); self.TableauChansons.heading("Album", text="Album")
        self.TableauChansons.column("Durée", width=70, anchor='center'); self.TableauChansons.heading("Durée", text="Durée")
        self.TableauChansons.column("URI de Piste", width=100, anchor='center'); self.TableauChansons.heading("URI de Piste", text="URI de Piste")
        self.TableauChansons.column("VidéoYT", width=300, anchor='center'); self.TableauChansons.heading("VidéoYT", text="Vidéo Youtube équivalente")
        self.TableauChansons.column("LienYT", width=150, anchor='center'); self.TableauChansons.heading("LienYT", text="Lien de la vidéo")
        self.TableauChansons.grid(row=1, column=0, columnspan=4, sticky='n', pady=5)
        self.vsb = ttk.Scrollbar(self, orient="vertical", command=self.TableauChansons.yview)
        self.vsb.grid(row = 1, column = 5, sticky="ns")
        self.TableauChansons.configure(yscrollcommand=self.vsb.set)
        self.TableauChansons.bind("<Double-1>", self.ChangerValeur)
        self.ajouterPistes()

    def ajouterPistes(self):
        for i in range(len(self.contenuPlaylist)):
            chanson=self.contenuPlaylist[i]
            self.TableauChansons.insert(parent='', index=END, values=[chanson.Titre, chanson.ArtistePrincipal, chanson.album, chanson.Duree, chanson.lien, chanson.NomVideo, chanson.LienVideo], iid=i, tag=str(i))
            if chanson.telechargee:
                self.TableauChansons.tag_configure(str(i), background="#83A183")

    def chercherYT(self): #? Chercher les equivalents YT de TOUTES les chansons.
        assert len(self.contenuPlaylist) == len(self.TableauChansons.get_children())
        for i in range(len(self.contenuPlaylist)):
            BoumBoumTypeMusic = self.contenuPlaylist[i]
            BoumBoumTypeMusic.searchYt()
            if BoumBoumTypeMusic.liensValables != [] and not BoumBoumTypeMusic.telechargee:
                NouvelleValeur = self.TableauChansons.item(i)['values']
                NouvelleValeur[5], NouvelleValeur[6] = BoumBoumTypeMusic.BestBanger[0], BoumBoumTypeMusic.BestBanger[1]
                self.TableauChansons.item(i, values=NouvelleValeur)
            elif not BoumBoumTypeMusic.telechargee :
                self.TableauChansons.tag_configure(str(i), background="#fd7676")

    def sauver(self): #? Enregister lensemble des infos dans un fichier json pour pouvoir le rouvrir par la suite.
        if not self.contenuPlaylist != [] :
            raise AssertionError('\n'*10+"La playlist est vide, tu veux que je sauvegarde quoi ?")
        Donnees={'NomPlaylist' : self.contenuPlaylist[0].NomPlaylist}
        for i in range(len(self.contenuPlaylist)):
            BangerANePasOublier = self.contenuPlaylist[i]
            Donnees[str(i)] = {'titre':BangerANePasOublier.Titre, 'ArtistePrinc' : BangerANePasOublier.ArtistePrincipal, 'album' : BangerANePasOublier.album, "durée" : BangerANePasOublier.Duree, 'Pochette' : BangerANePasOublier.Pochette, 'uriChanson' : BangerANePasOublier.lien, 'NomVideo' : BangerANePasOublier.NomVideo, 'LienVideo' : BangerANePasOublier.LienVideo}
        import json
        Fichier = asksaveasfilename(filetypes=[("Javascript Object Node", '*.json')], initialfile='BoumBoumMusicCollection.json')
        print(Fichier)
        with open(Fichier,'w') as f:
            json.dump(Donnees,f,indent=4, ensure_ascii=False)
    
    def importer(self): #? Enregister lensemble des infos dans un fichier json pour pouvoir le rouvrir par la suite.
        import json
        with open(askopenfilename(filetypes=[("Javascript Object Node", '*.json')]),'r') as f:
            Donnees = json.load(f)
        self.contenuPlaylistnu = []
        for i in range(len(Donnees)-1):
            BangerASeRememorer = Donnees[str(i)]
            self.contenuPlaylist.append(Chanson(BangerASeRememorer["titre"],BangerASeRememorer["ArtistePrinc"], BangerASeRememorer["album"], BangerASeRememorer["durée"], BangerASeRememorer["Pochette"], BangerASeRememorer["uriChanson"], Donnees["NomPlaylist"], NomVideoYT=BangerASeRememorer["NomVideo"], LienVideoYT=BangerASeRememorer["LienVideo"]))
        self.LancerTableauDesChansons()

    def ChangerValeur(self, event): #* Comment le "event" ne sert à rien...
        ChansonATelechargerMalgreTout = self.contenuPlaylist[int(self.TableauChansons.selection()[0])]
        ChansonATelechargerMalgreTout.telechargee = not ChansonATelechargerMalgreTout.telechargee
        if ChansonATelechargerMalgreTout.telechargee:
            self.TableauChansons.tag_configure(self.TableauChansons.selection()[0], background="#98b898")
        else :
            self.TableauChansons.tag_configure(self.TableauChansons.selection()[0], background="#faf8ca")
        for item in self.TableauChansons.selection():
            self.TableauChansons.selection_remove(item)


    def modifier(self):
        global BangerThatNeedsHelp, Brevassistance, Valeurs
        if not len(self.TableauChansons.selection())!=0 :
            raise AssertionError("Il faut sélectionner une chanson pour que ça marche")
        BangerThatNeedsHelp = self.TableauChansons.selection()[0]
        Valeurs = self.TableauChansons.item(BangerThatNeedsHelp)['values']
        Brevassistance = Tk()
        ttk.Label(Brevassistance, text = str(Valeurs[0:3])+"; lien Youtube : ").grid()
        self.DolipraneLikeSolution = Entry(Brevassistance, width=25)
        self.DolipraneLikeSolution.insert(0, "/watch?v=")
        self.DolipraneLikeSolution.grid()
        ttk.Button(Brevassistance, text='Valider', command=self.Valider3).grid()

    def Valider3(self):
        self.DolipraneLikeSolution = self.DolipraneLikeSolution.get()
        Brevassistance.destroy() #Aïe, j'ai mal. J'ai beau être matinal, j'ai mal
        self.contenuPlaylist[int(BangerThatNeedsHelp)].LienVideo = self.DolipraneLikeSolution
        try:
            DLC = (YoutubeSearch('http://youtube.com'+self.DolipraneLikeSolution, max_results=1).to_dict()[0])
        except:
            pprint(YoutubeSearch('http://youtube.com'+self.DolipraneLikeSolution, max_results=1).to_dict())
        self.contenuPlaylist[int(BangerThatNeedsHelp)].NomVideo = DLC["title"]
        Valeurs[5],Valeurs[6] = self.contenuPlaylist[int(BangerThatNeedsHelp)].NomVideo , self.DolipraneLikeSolution
        self.TableauChansons.item(BangerThatNeedsHelp, values=Valeurs)
        self.TableauChansons.tag_configure(BangerThatNeedsHelp, background="#faf8ca")

    def telechargerSelection(self):
        for idBanger in self.TableauChansons.selection() :
            if not self.contenuPlaylist[int(idBanger)].telechargee :
                self.contenuPlaylist[int(idBanger)].Telecharger()
                self.TableauChansons.tag_configure(idBanger, background="#759f75")

    def toutTélécharger(self):
        for ApprovedBanger in range(len(self.contenuPlaylist)):
            if not self.contenuPlaylist[int(ApprovedBanger)].telechargee :
                self.contenuPlaylist[int(ApprovedBanger)].Telecharger()
                self.TableauChansons.tag_configure(ApprovedBanger, background="#759f75")

fen = fenetre()
fen.mainloop()