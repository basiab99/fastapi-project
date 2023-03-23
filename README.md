# fastapi-project

Code in FASTAPI consisting of three endpoints. 

1. Endpoint checking if the number is prime (range 9223372036854775807) using GET.
GET <host>/prime/<number>
We do not assume the correctness of the data, checking if the data is in the correct range.

2. Endpoint to return a picture with inversed colors using POST 
POST <host>/picture/invert

3. Endpoint returning the current time  after authentication, also in the POST.

The whole app was deployed via the Heroku platform and a performance test report was made. Due to a policy change on the Heroku platform, access to deploy has expired, so a new solution is being sought to redeploy the application.
