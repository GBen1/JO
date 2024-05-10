from django.test import TestCase, Client
from django.urls import reverse 
import os
from io import StringIO
from django.contrib.auth.models import User
from utilisateur.models import Offres,Panier,Order
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from JO.forms import RegistrationForm,VerifyTicketForm,CreateOffre,ModifyOffre
from django.contrib.auth.views import LoginView

# Create your tests here.

#TEST MODEL USER
class ModeltestCaseUser(TestCase):
    
    def setUp(self):
        
        self.data = {
            'username' : 'JDUPONT',
            'last_name' : 'Dupont',
            'first_name' : 'Jean',
            'email' : 'aadt@hotmail.fr',
            'password' : 'nkjsabvhgaBHJVH(46*)'
        }

        self.user = User.objects.create_user(**self.data)
        self.x = User.objects.get(username = "JDUPONT")
        
    #On vérifie qu'un utilisateur a bien été créé dans la table user de la base de données avec le username:
    # "JDUPONT"
    def test_user(self):
        self.assertEqual (self.x, self.user)

    #On vérifie que toutes les valeurs envoyées sont bien présentes la base de données
    def test_user_last_name(self):
        self.assertEqual (self.x.last_name, self.user.last_name)
    def test_user_first_name(self):
        self.assertEqual (self.x.first_name, self.user.first_name)
    def test_user_email(self):    
        self.assertEqual (self.x.email, self.user.email)
    def test_user_password(self):    
        self.assertEqual (self.x.password, self.user.password)
#TEST MODEL OFFRES     
class ModeltestCaseOffres(TestCase):
    
    def setUp(self):
        
        self.data = {
           'libelle' : 'superoffre',
           'description' : 'ceci est une superoffre',
           'prix' : 50,
           'image' : 'img4.png'
        }

        self.offres = Offres.objects.create(**self.data)
        self.x = Offres.objects.get(libelle = "superoffre")
        
  #On vérifie qu'une offre a bien été créé dans la table Offres de la base de données avec le libellé:
    # "superoffre"
    def test_offres(self):
        self.assertEqual (self.x, self.offres)

    #On vérifie que toutes les valeurs envoyées sont bien présentes la base de données
    def test_offres_description(self):
        self.assertEqual (self.x.description, self.offres.description)
    def test_offres_prix(self):    
        self.assertEqual (self.x.prix, self.offres.prix)
    def test_offres_image(self):    
        self.assertEqual (self.x.image, self.offres.image)  

        #TEST MODEL OFFRES     
#TEST MODEL PANIER 
class ModeltestCasePanier(TestCase):
    
    def setUp(self):
        
        self.data = {
    'owner' : 'JDUPONT',
    'libelle' : 'SUPER_ITEM',
    'item' : 8,
    'prix' : 100

        }

        self.Panier = Panier.objects.create(**self.data)
        self.x = Panier.objects.get(owner = "JDUPONT")
        
  #On vérifie qu'un panier a bien été créé dans la table Panier de la base de données avec le owner:
    # "JDUPONT"
    def test_Panier(self):
        self.assertEqual (self.x, self.Panier)

    #On vérifie que toutes les valeurs envoyées sont bien présentes la base de données
    def test_Panier_libelle(self):
        self.assertEqual (self.x.libelle, self.Panier.libelle)
    def test_Panier_item(self):
        self.assertEqual (self.x.item, self.Panier.item)
    def test_Panier_prix(self):    
        self.assertEqual (self.x.prix, self.Panier.prix)
#TEST MODEL ORDER 
class ModeltestCaseOrder(TestCase):
    
    def setUp(self):
        
     self.data = {
    'owner' : 'JDUPONT',
    'libelle' : 'SUPER ITEM',
    'item' : 12,
    'prix' : 150,
    'message' : 'Billet n°113 valide pour Jean Dupont : Offre Familiale',
    'PUBKEY' : 'aadt@hotmail.fr_229345500.PEM',
    'QRCODE' : 'aadt@hotmail.fr_offre-familiale_113.png',
    'HEXA' : b'w\x9a\xd2\xd4\x12\xd9\x15\xbeDJ\x7fk/\x9d\xf10\xeeG\'M,\xd0\xe6\x84\xa3\x1c\xbe\xd2"p\xcb*t\x01\xbd=\xf2\x0c\xea9O\n\x8d\x9e\'_xQ9\xeb<\xb2;w\xdab\n\xe3#=\x87\xfd\x04\xc9t-\xfcG\xad\x1ce"\xc22\xd9\xab\xb8N^\x10-(J|\xfa\x81\xa5\xa1x\\Y\xcf\x02\xd5\xfc\x1b\x134\xd3\xed\xa3\xe8\xc7s\x08\xeb$\xfcs\x82=9\xf5\xffY6g+\xc7U\xca\xffvZ\xc7\xbap\xdb\xbe\xcb\xd8m\x9f\xd0\nK\xbe\xbdf\x17[\x8d\xd0I\xe3\xd0\xedu?Fg\xe34%\xe8\xc5\x1cV\xe6\x03\xcd\xf8p\x91\xd71\x81\xc0J!\x9b\xfa\xe3\xf0.\x0b\xf2n7\x06(\x0c\xcfS\x8c\xec\xcd\x00\x9e\'q\xbch-\xe4\x98\x19!*;}^\xc5\x9cN\xebS\x17\xe2=G\xfft\xfb\x1aU2W\nx+\xc2wQ>\xae{|\xb6\xfc2?\xb4\xc8\xec\xcc$\xa6\xb9\x19w\xa1\x0c\xf9\xdb\x0bs\xfa\x1c\xeb\x0c\x81\xe5\xc5<w)'

        }

     self.Order = Order.objects.create(**self.data)
     self.x = Order.objects.get(message = "Billet n°113 valide pour Jean Dupont : Offre Familiale")
        
  #On vérifie qu'un Order a bien été créé dans la table Order de la base de données avec le message:
    # "Billet n°113 valide pour Jean Dupont : Offre Familiale"
    def test_Order(self):
        self.assertEqual (self.x, self.Order)

    #On vérifie que toutes les valeurs envoyées sont bien présentes la base de données
    def test_Order_owner(self):
        self.assertEqual (self.x.owner, self.Order.owner)
    def test_Order_libelle(self):
        self.assertEqual (self.x.libelle, self.Order.libelle)
    def test_Order_item(self):    
        self.assertEqual (self.x.item, self.Order.item)    
    def test_Order_prix(self):    
        self.assertEqual (self.x.prix, self.Order.prix)    
    def test_Order_PUBKEY(self):    
        self.assertEqual (self.x.PUBKEY, self.Order.PUBKEY)    
    def test_Order_QRCODE(self):    
        self.assertEqual (self.x.QRCODE, self.Order.QRCODE)    
    def test_Order_HEXA(self):   
        c = self.x.HEXA.encode()
        ciphertext = c.decode('unicode-escape').encode('ISO-8859-1')
        ciphertext = ciphertext[2:-1] 
        self.assertEqual (ciphertext, self.Order.HEXA) 

#TEST FORM 

class FormtestCaseRegistrationForm(TestCase):


    def test_valid_form(self):
        form = RegistrationForm( 
            data={  
                'Nom' : 'Dupont',  
                'Prénom' :'Jean',   
                'Mot_de_passe' : 'nkjsabvhgaBHJVH(46*)',  
                'Confirmer_Mot_de_passe' : 'nkjsabvhgaBHJVH(46*)',
                'E_mail' : 'aadt@hotmail.fr' 
                }         
                )
        self.assertTrue(form.is_valid())

    def test_invalid_form_confirmation_mdp(self):
        form = RegistrationForm( 
            data={  
                'Nom' : 'Dupont',  
                'Prénom' :'Jean',   
                'Mot_de_passe' : 'nkjsabvhgaBHJVH(46*)',  
                'Confirmer_Mot_de_passe' : 'BONJOUR',
                'E_mail' : 'aadt@hotmail.fr' 
                }         
                )
        self.assertFalse(form.is_valid())   

    def test_invalid_form_pas_de_chiffre(self):
        form = RegistrationForm( 
            data={  
                'Nom' : 'Dupont',  
                'Prénom' :'Jean',   
                'Mot_de_passe' : 'nkjsabvhgaBHJVH(*)',  
                'Confirmer_Mot_de_passe' : 'nkjsabvhgaBHJVH(*)',
                'E_mail' : 'adth@hotmail.fr' 
                }         
                )
        self.assertFalse(form.is_valid())  

    def test_invalid_form_pas_de_maj(self):
        form = RegistrationForm( 
            data={  
                'Nom' : 'Dupont',  
                'Prénom' :'Jean',   
                'Mot_de_passe' : 'nkjsab44*vhga',  
                'Confirmer_Mot_de_passe' : 'nkjsab44*vhga',
                'E_mail' : 'aadt@hotmail.fr' 
                }         
                )
        self.assertFalse(form.is_valid())  
 
class FormtestCaseAuthenticationForm(TestCase):
 
   def setUp(self):
    self.data = {
            'username' : 'JDUPONT',
            'last_name' : 'Dupont',
            'first_name' : 'Jean',
            'email' : 'aadt@hotmail.fr',
            'password' : 'nkjsabvhgaBHJVH(46*)'
        }
    self.user = User.objects.create_user(**self.data)
    self.x = User.objects.get(username = "JDUPONT")
 
    def test_valid_form(self):
        form = AuthenticationForm( 
            data={  
                'username' : 'JDUPONT',  
                'password' : 'nkjsabvhgaBHJVH(46*)'
                }         
                )
        self.assertTrue(form.is_valid())

class FormtestCaseCreateOffre(TestCase):
     

    def test_valid_form_create_offre(self):

        self.image_file = open(
        os.path.join("/home/ubuntu/JO24/static/img/test.png"), "rb"
        )
                
      

        data={ 
            'libelle' : 'SUPER_OFFRE',
            'description' : 'Ceci est une super offre',
            'prix' : 100, 
          
            }    
        
        files_data = {
             'image': SimpleUploadedFile(
                  self.image_file.name,
                  self.image_file.read()
            )
        }
        form = CreateOffre(data=data,files=files_data)
        self.assertTrue(form.is_valid())  

class FormtestCaseModifyOffre(TestCase):

 def test_valid_form_modify_offre(self):

        self.image_file = open(
        os.path.join("/home/ubuntu/JO24/static/img/test.png"), "rb"
        )
                
      

        data={ 
            'libelle' : 'SUPER_OFFRE',
            'description' : 'Ceci est une super offre',
            'prix' : 100, 
          
            }    
        
        files_data = {
             'image': SimpleUploadedFile(
                  self.image_file.name,
                  self.image_file.read()
            )
        }
        form = ModifyOffre(data=data,files=files_data)
        self.assertTrue(form.is_valid())  

class FormtestCaseVerifyTicketForm(TestCase):
  def test_valid_form(self):
        form = VerifyTicketForm( 
            data={  
                'Billet' : 'dNBHU46445VHGJKJHVzdzfzeg85675547ze',  
                }         
                )
        self.assertTrue(form.is_valid())

# TEST VIEWS

class  ViewstestCaseRegistrationAndAuth(TestCase) : 
    # CREATION USER
    def setUp(self):
        
        self.client = Client()

        self.user_data = {   
            'username' : 'JDUPONT',
            'last_name' : 'Dupont',
            'first_name' : 'Jean',
            'email' : 'aadt@hotmail.fr',
            'password' : 'nkjsabvhgaBHJVH(46*)'
        }
    
        self.user = User.objects.create_user(**self.user_data)

    #Verification de l' accès à la page d' enregistrement
    def test_register_view(self):

        url = reverse('registration')

        response = self.client.get(url)

        self.assertEqual(response.status_code,200)


    def test_authentication_view(self):
        #On se connecte
        client = Client()
        client.force_login(self.user)
        response = client.post(reverse('login'))
        #On vérifie la redirection après connection
        self.assertEqual(response.status_code, 302)




