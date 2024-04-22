import json
from time import sleep
import websockets
import asyncio
import polyline
 
# The main function that will handle connection and communication
# with the server

geometry = "}_tnA_kzgNTBIyC@q@?_AFaBZ{DPcBLwAJu@LkBRmCb@kAzAiFDyACi@MkM?w@Hs@TmA~@mDtAoFn@oB`A_C`BeDR]d@y@v@aBTm@L]rAgEb@wARk@^i@h@oALc@RmA\\wALe@FWv@cD^oBZeB@W@[@_@E_@[sAa@aAMYTIT_@d@_DNm@h@mB`AkDh@wBXo@H[r@uBV{@~@cDp@_ChAcExBcH`@kAtAuDRe@r@uBfAiDh@mBf@uCtAwFZ_Af@cBFUFW@Eh@sBtCoJ`@wAb@}Ad@iB`@qBPoAr@qI~@mNl@cH@OnAwP`@sEBqIAiD?OEcAGgIAsB?qDFkARq@Xm@V{@pAiDpCaHJQX{@Vo@P{@@o@GsAC{@Cw@@aALiA?e@@_AD}@No@vBoEnBoEnBgEl@uAzCyGxD}I|FaMvB}Eh@kAVk@z@kB~DcJxD_IrBuEvCqGrFuLrDkIfByDf@}@Tk@|ByERc@LS`AqB~@cEPo@N[t@u@h@WvFqCh@_@zAwABGfAaCp@{AhEsJXm@HMjCwF~BcFfAgBl@o@x@m@`Ag@pOoIZM^Kf@E~DCVE`A[hAg@HODg@Bm@@UAqBGeBEuB?cH@qAEy@DkADqA@UJgDLcAJc@NSbA}@NSRe@D]@cAA_@DcF?wAUiB}@sLU}Be@}BWgAwAgGqB}HgByFKq@Ea@QiCGa@K[kBeF_AiCi@_CS}@u@eDm@gCk@uBQw@?c@FMH?FJNh@v@bDtBvJz@hDx@dCl@dBh@r@l@hBLXd@E~A_@d@OL[MoBEg@Am@Dc@`AeCBEn@{@hAk@`F_BxAe@TMD[LuCCu@}@kBAKAUdQfC|BZfChAtCdDf@b@tFdDpG|CzBv@zAT`CBnBI^AdCUnA]^KrUgOFENKHJvD`AlE`A`Bd@vA\\v@JdBThANXDdDf@xBRp@DvB@tC?tD?tC@j@?h@CfCOpAUvFwAjGqBh@O`@M|Aa@|GoBjAe@rAo@b@If@Ab@FnE~A|@XvEpAd@J~@J|Bp@zA`@bAFv@T|ATrGvBF@l@RPFJL@FMl@q@tB_ArBqAzBq\\jb@X\\lRwUlJeLr@cAdAiBV[`@[XYJSJ_@HUN_@XIL?zAd@fKvCtBfAb@Lv@RRHf]bKdJjCbI`CdCx@lGbBzDfAbFbB|ARtIdCdBd@D_C?g@Ak@Ae@?WOwIAQQcFC_@K_CAUC]SyDAQOcDASEy@C_@OeDASY{FAWQkDAUMcFAa@EsA?OCq@Aa@]wMAc@o@a_@OmEOqEC_D?qADqADo@b@aGl@wHJeA~AkLO_@MYOO_MoCkBe@yBs@wF{A{DqAiCs@HYrC~@PFjHzBtBj@vDbAr@NrEdAHB~GxAlHvBvGnBnB|@^RRN~AbBpDjEp@r@RNX\\l@d@RJd@Z`A\\n@NjANrIzApE|AxSdI`KtDZH|DlAdCr@t@NvA\\|HvAh@HdAP|@JrCRdBHxE^l@DzF^nBJd@DvDVnAJjM~@jIh@zJr@pEV~ANpDXrBLJ@t_@zCvBRbDVlCNrFNhGNzR`@R@zADpCFdJTfLV|JR`H`@xPFhGBjCNlAHhHnAfANt@?hDDlBCbQEtHEnBGfDQxAC|CKD?V?vEDvGd@dEN`@@?RAJO?"
cordinates = polyline.decode(geometry, 5)
# print(cordinates)

async def ws_client():
    print("WebSocket: Client Connected.")
    # url = "ws://192.168.29.180:8000/ws/buslocation/2"
    url = "wss://congenial-adventure-v7ww59w77r4fpvwg-8000.app.github.dev/ws/buslocation/2"
    # Connect to the server
    async with websockets.connect(url) as ws:

       
        # for cor in cordinates:
        #     loc = { "lat" : cor[0], "lang" : cor[1] }
        #     await ws.send(json.dumps(loc))
        #     msg = await ws.recv()
        #     print(msg)
        #     sleep(2)
        while(True):
            loc = { "lat" : cordinates[0][0], "lang" : cordinates[0][1] }
            await ws.send(json.dumps(loc))
            msg = await ws.recv()
            print(msg)
            sleep(2)
 
        
        # while True:
        #     msg = await ws.recv()
        #     print(msg)
 
# Start the connection
asyncio.run(ws_client()) 