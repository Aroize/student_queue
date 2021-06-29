import sys
sys.path.insert(0, "../api")

from security import *
from keys import *
from jwt import JWT, jwk_from_dict

if __name__ == '__main__':
    access_secret = jwk_from_dict({
        "p": "9eOWmDLGKxGf4dO3TqmKIRkZxat4JIe1hShDDbpkK-yKmVYpqyGOjo-6MB4fDz68bvrsx2-kP5CWrMXsSUIB5KpbRtrzQgmAw70JEN3OfSsx-BICJa50u0R0Ju44zQ1r4NSE8e3jkTth21vHRMW2u5B8ftmlgpA6Pt3hrMpIFkc",
        "kty": "RSA",
        "q": "77OTN7hxANP_Wk_JJ3C6XOShO0PuU7WGaUfa8Y-vh2eYHX3WFUDRKDDVEYS-ICwHS4aXF-adMNKHj-jB65Fq4IXYNexPddVOmWR_IOkaBF0M05-LWLo_f6TJgTLXc7KSWLqpxACb4vZiV15c-P6ylHhpmlqAPHeRTqS0p_QQeK8",
        "d": "0TnpkYcmqnjOi9eMDTldqipz7uHgTsMW9h0Ge11xsaqY55WLqzk7Oe88p-vIo8lGWqP_wDoY1VIrI2KsXBY1W7C5qchMx1xx5W5oSM_H5E4WdVU7ECrkbhgNs6tKlS4H_pnsdQaoR4mu497_QcAQRKJnBwVk49y7e_y5SqTZ3eNtqB9OaGEfB_S6YoZiMmUpIOTsVmCwnG7PV3_G4lF-MK9ZI862GtTkvHAeT-_uBjf8hrtP2NbxZBmvHr8kie-MjG_Yxo8Y6Ai7qU4sFi9mIit2Lq9_CUpndG88xiappzDbXLv3y56pG76AqC0nivFeLppDBngh5lr9XYtAq2EeZQ",
        "e": "AQAB",
        "use": "sig",
        "kid": "oQb0WuVBV_nz5rVTMiluz3gYQowLVI-scW-D-bGtU-U",
        "qi": "8VloyhszhGb14_of07ieYzFQEMCSg1hiqhltXDo8OD1-Kl9veHhTz7OGnyxv9_RH8AiLK7mlJACP2RGRFfc-mJfO7fP-cOO0rrdXJiX8AdK7eT9ALUknai3sfprPhvH4hwMxANCPL9WwKaU22BBy_Nilfmio_9e8ysO5S1dSx1A",
        "dp": "4ZlDFTcYjHFqMIbQGzMAEaf29l6BJ3r_t0EebF0EBSzMaS0do-5w3inOWNF6C8Gyn1xHnB-5IbzmEXSyevA9zm_iuRqvr3oKkwxAYiIvjrXv7buQDsSGQz7mFsXghXn37Vru8w0hCqHiAaGuLVH9ew9wue20phrv5bgrkx4wj4c",
        "alg": "RS256",
        "dq": "K8meJxumaQRRLWpN0MqjAL0zRuRN8TTD7Q-XS3F4G0AtZZXLOe6xRqpFAgJByRbB7mYTy-Xw6S5MXVmjsyjJYWKR8KfOjDP_O75ECvsKKanl4fLPPdIoL2Um-lcTTKteWJ8gzBFgaMGhjVxLl6DPdpfYkr3dly4weTFVXykSqTk",
        "n": "5jv1IZhZYR7Ca2ittdvPrxZdccYLolxqG2F6Og3Na9Fu_WbCOx_FfI6L0szFDdyq8EPbNOZY7nQ0e0k2rum-qfEovPdbuxN5Di6GUl3EtUxHSEAiRduCVgwp4egnTn7rcYZXsQajVxTI3MqSRyK6FLQ41L0GtORy36WVk9GCuwTxRG6KqEQPUk5cpyOwDX-fjIuPEl4urCxkRpUMJXOuhhgNqkYXFvZyy702voire4UQuNohhj8TbQE4Lwt6h3SNbekji5XY2Sfz2-SSt1MFk8oAQDK5JDcUvZbYYEgv7OaStwwaKhEtW8OxUoKzp9kdWQ2U_Or-MGFTPBH-IiiCiQ"
    })

    refresh_secret = jwk_from_dict({
        "p": "_YLWw01HI-o4gztx-rFH61eqQRB6G1e3n3fbnZe0bz2JBlicWHntighjNh1_nQMejwbkHK5TNRHA9lW3Tq5qRAiWZP3_5Kpqqf7vM9thPwR5DfnjFlKqPF21OP1VoEJYvjSaQqjFpP3dAAJxaFOH-XPYdp0TdgWpSldfLD_uYYk",
        "kty": "RSA",
        "q": "5HAu2_RDGnkDUnHaiWSLeNAdzQDPhNigN1Ccsh4IYXetAicaRTsqbuakEm0pyZobYankYKwkxseEfYgjqcnojmoH1JaPMSUpk9BRIGfffpfE2X-xgpkWoCBX1IEoCfZarnFBs_kbjYZ3LKHymUb1drjMlBn7Rf3x3IgSTvwSQfE",
        "d": "zT91-yqbg5CrjYBOoVrQyNbPwgAQYC7eesNsanc-MQ4xFK0EK_9ClC4JxQHskLFBVgySTcGQNGblm_VXC0phaTVT3VMhJ1wp9WXlyqML8Q3lXl5aRT5nNzLJlEENefDHHP0NmwIEEDfXsy03Tkmb40j9DlZ5lMt8xuT7XmGgp2sDoeDwp8fkY4vP1ks3jQNPQBO6hWw1iMxEtZnwd4sDxKo_0rR2altLlHIvvTNuz0Ye17mvELfEi_rXZHC4Jmw7OpGr9duyG2fgChR3DvkMHv_ErpX6ZVPKtfTMW_1Po4sJVpLzBbpAsVh98ai928lbX0G4xDxmCCl4193WgeKtAQ",
        "e": "AQAB",
        "use": "sig",
        "kid": "5qO59wE3dklboUaK8IXmYDUNleRnAFGQAVXR168FfCM",
        "qi": "rehGVtOrTUe_p3NJh6PRIpb-dBXB4LoUR1NclDesiBTYUpp3xsWxOoQQxbz6yaF0eqdA2r8B-w6BM4kEaEKjFIERbUtg3FMbDqR7yO44eNJjdQH-Xd0JkkSwANyjVFmCm5MhHPvCiEn6yy4H743swSovXuEfVTr5LlsV9_8HxRE",
        "dp": "kJ30-dC5xok019gvez1qs5x86UUHA1YU0AnF5K7IJbVK163w8qALm_SQ9Cv7wownAJyDwMDJgrqwA1Z-jYn94PWtJcuoEMAOvQ9LUZ_SZ-qbTBfDLdbWej1SxkHueM-gZFEJtwEkTqzrR7gdDdCo_urRD0kn8unj2x7gkhOeX1E",
        "alg": "RS256",
        "dq": "Ki4AqQJ4JXo0v9Nf-8CB9EPRTNoadzgclTogRM9A0uZrHpujwSbElgemQfTAI4Z-CdF55tPCUqXic99gXmh2tV0kpv9J31QyUiXD5Qzo-pIBefuXBjtILzbpoMZcY0KGyfEFpbqYeNBcTvR0PBMbHdnPhIUrnWffcc36O3VV1bE",
        "n": "4jee6zmtJDmv0_cQFUHNZylBc8SY9W5-SgqoBFr_wGd5NKmYzGUDQs_VGSICgiFdsDSp4PePvoWGEd73NhstihTyCVjCb84QhZDrp9ToH5dkcW8fLVH3OWFy507EoEB68uvamJgpVxhgR2Kk-dAeFs3yyd0O3gTPux-M1wJuwNj8sFpejQfuuHHLVg2FRBFsNlQxr4kHfmwzZ_c_jecosGFw5-KI3WPFTcTsN39fcdMYrWAq8ZHuy0bLC5YfjLBolaZNy7vZ67FBryLZ_8xh7OwPRAjKzrGPfu-N6kSBrZm5yb2XoGVCTpHXC6AY3xY4UglPzBkesXw1u1Vnbc-a-Q"
    })

    jwt_controller = JwtTokenControllerImpl(access_secret, refresh_secret)

    base_credentials = Credentials(228)

    credentials = jwt_controller.generate_full_credentials(base_credentials)

    print(credentials.id)
    print(credentials.access_token)
    print(credentials.refresh_token)

    print(jwt_controller.is_access_token_valid(credentials))

    print(jwt_controller.is_refresh_token_valid(credentials))
