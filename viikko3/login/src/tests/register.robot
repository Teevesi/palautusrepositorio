*** Settings ***
Resource  resource.robot
Suite Setup     Open And Configure Browser
Suite Teardown  Close Browser
Test Setup      Reset Application Create User And Go To Register Page

*** Test Cases ***

Register With Valid Username And Password
    Set Username  jaakko
    Set Password  jaakko123
    Set Password Confirmation  jaakko123
    Click Button  Register
    Register Should Succeed

Register With Too Short Username And Valid Password
    Set Username  ja
    Set Password  jaakko123
    Set Password Confirmation  jaakko123
    Click Button  Register
    Registration Should Fail With Message  Username must have at least 3 characters

Register With Valid Username And Too Short Password
    Set Username  jaakko
    Set Password  jaa
    Set Password Confirmation  jaa
    Click Button  Register
    Registration Should Fail With Message  Password must have at least 8 characters

Register With Valid Username And Invalid Password
    Set Username  jaakko
    Set Password  jaakkoka
    Set Password Confirmation  jaakkoka
    Click Button  Register
    Registration Should Fail With Message  Password must contain at least one number

Register With Nonmatching Password And Password Confirmation
    Set Username  jaakko
    Set Password  jaakko123
    Set Password Confirmation  jaakko456
    Click Button  Register
    Registration Should Fail With Message  Password and password confirmation do not match


Register With Username That Is Already In Use
    Set Username  kalle
    Set Password  kalle123
    Set Password Confirmation  kalle123
    Click Button  Register
    Registration Should Fail With Message  Username already exists

*** Keywords ***

Set Username
    [Arguments]  ${username}
    Input Text  username  ${username}

Set Password
    [Arguments]  ${password}
    Input Password  password  ${password}

Set Password Confirmation
    [Arguments]  ${password_confirmation}
    Input Password  password_confirmation  ${password_confirmation}

Register Should Succeed
    Welcome Page Should Be Open

*** Keywords ***

Reset Application Create User And Go To Register Page
    Reset Application
    Create User  kalle  kalle123
    Go To Register Page


Registration Should Fail With Message
    [Arguments]  ${message}
    Register Page Should Be Open
    Page Should Contain  ${message}



