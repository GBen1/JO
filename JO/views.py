from datetime import datetime
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django.contrib.auth.views import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import views

from JO.forms import RegistrationForm
from JO.forms import VerifyTicketForm
from JO.forms import CreateOffre
from JO.forms import ModifyOffre

from django.contrib.auth.models import User
from utilisateur.models import Panier
from utilisateur.models import stat_vente
from utilisateur.models import Offres 
from utilisateur.models import Order

import environ
env = environ.Env()
environ.Env.read_env()

from Cryptodome.PublicKey import RSA
from base64 import b64decode
from Cryptodome.Cipher import PKCS1_OAEP
from django.db.models import Sum
from pathlib import Path
import os
import sys
import subprocess
import random
import segno
import codecs



date = datetime.today()

def index(request):
    return render(request,"index.html")

def registration(request):
  form = RegistrationForm(request.POST)
  if request.method == "POST":
     if form.is_valid()  :
      #and not User.objects.filter(email=form.cleaned_data["E_mail"]).exists()
      User.objects.create_user (
          username = form.cleaned_data["E_mail"].lower(),
          last_name = form.cleaned_data["Nom"],
          first_name =  form.cleaned_data["Prénom"],
          email = form.cleaned_data["E_mail"].lower(),
          password = (form.cleaned_data["Mot_de_passe"]),
       )
      
      
      cle_rsa = RSA.generate(2048) 
      cle_privee = cle_rsa.exportKey("PEM",env('PEMKEY'), pkcs=1) 
      filepath = Path("/home/ubuntu/JO24/static/keys/PRIVKEY/"+User.objects.get(username=form.cleaned_data["E_mail"].lower()).PRIVKEY)
      #subprocess.call(['sudo', 'python3'] + sys.argv)
      fd = open(filepath, "wb") 
      fd.write(cle_privee) 
      fd.close() 
      #filepath.touch(mode=0o700)
      #os.chmod(filepath, 0o600)
      return HttpResponseRedirect('accounts/login/')
     else:
      return render(request,"registration.html", { "form":form})
  else: 
   form = RegistrationForm()
   return render(request,"registration.html", { "form":form})
    


def offres(request):
   form = VerifyTicketForm()
   data = Offres.objects.order_by('-id')
   result =""
   if request.method == "POST":
     

      if 'verifier' in request.POST:
       
        data2 = request.POST['Billet']
       
       # data2 = form.cleaned_data["Billet"] 
        if Order.objects.filter(HEXA=data2).count() == 1:
          a= Order.objects.get(HEXA=data2).HEXA
          c = a.encode()
          ciphertext = c.decode('unicode-escape').encode('ISO-8859-1')
          ciphertext = ciphertext[2:-1]
          user = Order.objects.get(HEXA=data2).owner
          cle = RSA.import_key(open("/home/ubuntu/JO24/static/keys/PRIVKEY/"+User.objects.get(username=user).PRIVKEY).read(),passphrase=env('PEMKEY'))
          cipher = PKCS1_OAEP.new(cle)

          #data2 = bytes(data2, 'utf-8')
          #data2 = bytes(data2, 'utf-8').decode('utf-8')
          #data2 = data2[2:len(data2)-1]
         # data2 = data2.replace('\\\\', '\\')
          #codecs.decode(data2, 'unicode_escape')
          #data2 = bytes(data2, 'utf-8')
          
          message_dechiffre = cipher.decrypt(ciphertext)         
          result = message_dechiffre.decode("utf-8")
          return render(request,"offres.html",{"data":data,"form":form,"result":result})
        else:
         result="Le billet n'existe pas ou n'est pas valide"
         
         return render(request,"offres.html",{"data":data,"form":form,"result":result})

      
      else:
       panier = Offres.objects.get(id=request.POST['pk'])
       return HttpResponseRedirect('accounts/login/',{"data":panier})
   
   else:
    data = Offres.objects.order_by('-id')
    return render(request,"offres.html",{"data":data,"form":form,"result":result})


def profile(request):
    data = Offres.objects.order_by('-id')
    data2 = Panier.objects.filter(owner=request.user.username).order_by('id')
    data3 = Order.objects.filter(owner=request.user.username).order_by('-id')
    data4 = stat_vente.objects.all().order_by('-somme')

    Somme = Panier.objects.filter(owner=request.user.username).aggregate(Sum('prix'))['prix__sum']
    #Somme = str(Somme)
   
    
    form = CreateOffre(request.POST,request.FILES)
    form2 = ModifyOffre(request.POST,request.FILES)

    if len(request.user.username) < 1 :
     return HttpResponseRedirect('/accounts/login/')
    elif request.method == "POST":
     #L' utilisateur procède au paiement
     if 'payement' in request.POST:
      Import_to_order = Panier.objects.filter(owner=request.user.username)
      Count_panier = Panier.objects.filter(owner=request.user.username).count()
      #On récupère la clé privée
      private_pem_key = RSA.import_key(open("/home/ubuntu/JO24/static/keys/PRIVKEY/"+User.objects.get(username=request.user.username).PRIVKEY).read(),passphrase=env('PEMKEY')) 
      #On recré une RSA key à partir de la clé privée pour pouvoir générer une clé publique
      modulusN = private_pem_key.n
      pubExpE = private_pem_key.e
      priExpD = private_pem_key.d
      primeP = private_pem_key.p
      primeQ = private_pem_key.q
      RSA_private_key = RSA.construct((modulusN, pubExpE, priExpD, primeP, primeQ))
      #On cré une clé publique à partir de la clé privée
      public_pem_key = RSA_private_key.publickey().exportKey('PEM')
      #On nomme le fichier qui détiendra la clé publique (si il n'existe pas déjà)
      if Order.objects.filter(owner=request.user.username).exclude(PUBKEY="").order_by('id').count() > 0:
        pub_file = Order.objects.filter(owner=request.user.username).exclude(PUBKEY="").order_by('id')[0].PUBKEY
      else:
        pub_file = request.user.username+"_"+str(random.randint(1,1000000000))+".PEM"
        filepath = Path("/home/ubuntu/JO24/static/keys/PUBKEY/"+pub_file)
        #On cré le fichier de clé publique (si il n'existe pas déjà)
        fd = open(filepath, "wb") 
        fd.write(public_pem_key) 
        fd.close() 


      #On met le contenu du panier en commande
      for z in range(Count_panier):
         
         AddCommande = Order(
         owner = Import_to_order[z].owner,
         item = Import_to_order[z].item,
         prix = Import_to_order[z].prix,
         libelle = Import_to_order[z].libelle,
         PUBKEY = pub_file,
          )
         AddCommande.save()
      #On supprime le panier
      Panier.objects.filter(owner=request.user.username).delete()

      #On cré le message du QRcode et on le met dans la table
      current_order = Order.objects.filter(owner=request.user.username,message='')
      count_order = Order.objects.filter(owner=request.user.username,message='').count()
      for a in range(count_order):
        update_order = Order.objects.get(id=current_order[0].id)
        update_order.message = "Billet n°"+str(current_order[0].id)+" valide: "+str(current_order[0].libelle)+" pour "+str(User.objects.get(username=request.user.username).last_name)+" "+str(User.objects.get(username=request.user.username).first_name)
        update_order.save()
      
     #On cré le QRcode
      current_QR_order = Order.objects.filter(owner=request.user.username,QRCODE='')
      count_QR_order = Order.objects.filter(owner=request.user.username,QRCODE='').count()
      
      for b in range(count_QR_order):
        update_QR_order = Order.objects.get(id=current_QR_order[0].id)
        cle = RSA.import_key(open("/home/ubuntu/JO24/static/keys/PUBKEY/"+current_QR_order[0].PUBKEY).read(),passphrase=env('PEMKEY'))
        cipher = PKCS1_OAEP.new(cle)
        ciphertext = cipher.encrypt(bytes(current_QR_order[0].message, 'utf-8'))
        qrcodename = request.user.username+"_"+current_QR_order[0].slug+"_"+str(current_QR_order[0].id)+".png"
        update_QR_order.QRCODE = qrcodename      
        update_QR_order.HEXA = ciphertext        
        update_QR_order.save() 

        qrcode = segno.make_qr(str(ciphertext))
        qrcode.save("/home/ubuntu/JO24/static/keys/qrcode/"+qrcodename,scale=5,)

      return render(request,"utilisateur/profile.html",{"form":form,"form2":form2, "user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
     elif 'delpanier' in request.POST:
      Delpanier = Panier.objects.get(id=request.POST['delpanier'])
      Delpanier.delete()
      Somme = Panier.objects.filter(owner=request.user.username).aggregate(Sum('prix'))['prix__sum']
      return render(request,"utilisateur/profile.html",{"form":form,"form2":form2, "user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
     elif 'addpanier' in request.POST:
        Addpanier = Panier(
          owner = request.user.username,
          item = request.POST['addpanier'],
          prix = request.POST['addpanier2'],
          libelle = request.POST['addpanier3'],
           )
        Addpanier.save()
        Somme = Panier.objects.filter(owner=request.user.username).aggregate(Sum('prix'))['prix__sum']
        return render(request,"utilisateur/profile.html",{"form":form,"form2":form2, "user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
     elif 'modify' in request.POST:
      if form2.is_valid():

        Offre = Offres.objects.get(id=request.POST['modify'])
        Offre.libelle = form2.cleaned_data["libelle"]
        Offre.description = form2.cleaned_data["description"]
        Offre.prix = form2.cleaned_data["prix"]
        Offre.image = form2.cleaned_data["image"]
        Offre.save()        
        return render(request,"utilisateur/profile.html",{"form":form,"form2":form2, "user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
      else:
        return render(request,"utilisateur/profile.html",{"form":form,"form2":form2, "user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
      
     elif 'create' in request.POST:       
       if form.is_valid():

         Offre = Offres(
		     libelle = form.cleaned_data["libelle"] ,
         description = form.cleaned_data["description"] ,
         prix = form.cleaned_data["prix"] ,
         image =form.cleaned_data["image"] ,
	       )
         Offre.save() 
         form = CreateOffre()
         form2 = ModifyOffre()
         return render(request,"utilisateur/profile.html", {"form":form, "form2":form2,"user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
       else:
         return render(request,"utilisateur/profile.html", {"form":form, "form2":form2,"user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
    
     else:
       Somme = Panier.objects.filter(owner=request.user.username).aggregate(Sum('prix'))['prix__sum']
     form = CreateOffre()
     form2 = ModifyOffre()
     return render(request,"utilisateur/profile.html", {"form":form, "form2":form2,"user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})
    else:
     Somme = Panier.objects.filter(owner=request.user.username).aggregate(Sum('prix'))['prix__sum']
     form = CreateOffre()
     form2 = ModifyOffre()
     return render(request,"utilisateur/profile.html", {"form":form, "form2":form2,"user":request.user.username,"data":data,"data2":data2,"data3":data3,"data4":data4,"sum":Somme})

  

#def login(request):
 #   if request.method == "POST":
 #     form = LoginForm(request.POST)
 #     if form.is_valid():       
 #      return HttpResponse("Login ok")
 #    return render(request,"login.html", {"form":form})
#    form = LoginForm()
  #  return render(request,"login.html", {"form":form})

   

def vue_de_test(request):
    return HttpResponse("<h1>Vue de test </h1>")


