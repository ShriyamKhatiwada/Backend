from firebase import firebase

firebase = firebase.FirebaseApplication("https://smart-park-815ad.firebaseio.com/", None)

data = {
    'Name':'Shriyam',
    'Email':'shriyam@gmail.com'
    }
result = firebase.post('/smart-park-815ad/Space1',data)
print(result)