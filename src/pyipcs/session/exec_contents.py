"""
pyIPCS Temporary SYEXEC EXECs
"""

# CLIST to run IPCS Subcommands
IPCSRUN = """PROC 0 SUBCMD()

IPCS NOPARM                 /* ENTER THE IPCS SUBCOMMAND */
                            /* TO START AN IPCS SESSION */
IF &LASTCC>8 THEN EXIT CODE(&MAXCC)

WRITE ___IPCS_SUBCMD___
WRITE &SUBCMD
WRITE ___IPCS_SUBCMD___

WRITE ___SUBCMD_START___
&SUBCMD
SET &RC = &LASTCC
WRITE ___SUBCMD_END___

WRITE ___SUBCMD_RC_START___
WRITE &RC
WRITE ___SUBCMD_RC_END___
"""

# REXX to run evaluate
PYIPEVAL = """/* REXX */
storage. = ''
ADDRESS IPCS
 
 
 
/* Obtain_Data: procedure expose storage. */
   /*-----------------------------------------------------------*/
   /* Function:  Obtain_Data                                    */
   /*                                                           */
   /*            Retrieve data from the dump.  Invoke the IPCS  */
   /*            EVALUATE subcommand as necessary to access     */
   /*            512-byte blocks of data from the IPCS dump     */
   /*            source and store the data in variable          */
   /*            "storage."  Callers of Obtain_Data must        */
   /*            request storage from the same address space.   */
   /*                                                           */
   /* Input:     Description of data to access:                 */
   /*                                                           */
   /*            Hex address of data.                           */
   /*            Decimal position from the hex address of the   */
   /*             first byte to access.                         */
   /*            Decimal length of the data to access.          */
   /*                                                           */
   /* Output:    Requested data is returned.                    */
   /*-----------------------------------------------------------*/
 
   arg ARGUMENTS
   PARSE UPPER ARG hex_address dec_position dec_length 

/* trace off           Suppress display of unsuccessful storage */
/*                              fetches once PF3 has been hit   */
   Numeric digits(10)
   ipcs_eval_limit = 512     /* The maximum number of bytes that
                                the IPCS EVALUATE subcommand can
                                access per invocation           */
   page_size = 4096          /* The size of a storage page      */
   first_index  = dec_position % ipcs_eval_limit /* Determine the
                                first 512 byte increment        */
   last_index  = (dec_position+dec_length) % ipcs_eval_limit /*
                                Determine the last 512 byte
                                increment                       */
   buffer = ''
   do i= first_index to last_index /* For each 512 increment    */
    if storage.hex_address.i = '' then do
 
    /*----------------------------------------------------------*/
    /* If the data has not yet been accessed, access it.        */
    /*----------------------------------------------------------*/
 
         hex_address_dot = ,
            hex_address||.    /* Indicate for IPCS that it is an
                                address                         */
        "EVALUATE"   hex_address_dot ,
                "POSITION("i*ipcs_eval_limit")" ,
                "LENGTH("ipcs_eval_limit")" ,
                "REXX(STORAGE(X))" /* Access the data by invoking
                                the IPCS EVALUATE subcommand    */
        if rc > 0 then do
 
        /*------------------------------------------------------*/
        /* If 512 bytes of data could not be accessed, determine*/
        /* if the data spans across a page.  If it does, attempt*/
        /* to access the data that resides in the first page.   */
        /*------------------------------------------------------*/
 
          address = x2d(hex_address)+i*ipcs_eval_limit
          new_length=page_size-(address//page_size)
          if new_length=0 | new_length >= ipcs_eval_limit then
            signal Access_Error
          "EVALUATE"   hex_address_dot ,
                  "POSITION("i*ipcs_eval_limit")" ,
                  "LENGTH("new_length")" ,
                  "REXX(STORAGE(X))" /* Access the data by invoking
                                the IPCS EVALUATE subcommand    */
          if rc > 0 then signal Access_Error
        end
        storage.hex_address.i = x   /* Save the data in a
                                variable so that it only needs to
                                be accessed once                */
    end
    buffer = buffer||storage.hex_address.i /* Augment the buffer
                                with the current data           */
   end                       /* For each 512 increment          */
   return_offset = (dec_position-first_index*ipcs_eval_limit)*2+1
   return_length = dec_length*2
   if return_offset-1 + return_length > length(buffer) then
 
   /*-----------------------------------------------------------*/
   /* Do not attempt to return more than what is in the buffer. */
   /*-----------------------------------------------------------*/
 
      signal Access_Error
   string = substr(buffer,return_offset,return_length)
   "NOTE '"string"'" /* Return
                                the appropriate data from the
                                buffer                          */
   return
 
Access_Error: nop
GEN$='IPCS Evaluate subcommand unable to access storage'
Call Put                    /*       Display GEN$            */
Exit 16
 
Put: procedure expose GEN$
/*-----------------------------------------------------------*/
/* Function:  Put                                            */
/*                                                           */
/*            Invoke the IPCS NOTE subcommand to transmit    */
/*            data to the terminal, IPCS print data set or   */
/*            both depending on the IPCS message routing     */
/*            default.                                       */
/*                                                           */
/* Input:     Data to transmit.                              */
/*                                                           */
/* Output:    Data is transmitted.                           */
/*-----------------------------------------------------------*/
 
"NOTE '"GEN$"' ASIS"
if rc>0 then Signal Put_Error
return
"""
