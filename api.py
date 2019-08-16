from urllib import request

headers = {
      'Authorization': 'Bearer VNEIADCZTTMUDAN7533X',
      'Content-Type': 'application/json'
    }

# def eventbrite_api_venue(venue_id):


#     req = request.Request(f'https://www.eventbriteapi.com/v3/venues/{venue_id}/', headers=headers)

#     response_body = request.urlopen(req).read()
#     print(response_body)

#     return response_body    

def eventbrite_api_request():
    """Request data from Eventbrite API with filters requested."""


    
    req = request.Request(f'https://www.eventbriteapi.com/v3/events/search/?q=dance&start_date.range_start=today', headers=headers)

    response_body = urllib.request.urlopen(req).read().decode('utf-8')
    
    print(response_body)

    return response_body