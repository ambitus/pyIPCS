"""
File for using JCL to create MockSubcmd Objects
"""

import warnings
from zoautil_py import jobs, datasets
from .mock_subcmd import MockSubcmd
from .conftest import TEST_HLQ

SUBCMD_JCL_OUTPUT_DSNAME = ".PYTEST.MOCKPY"

JCL_TEMP_DSNAME = ".ZOAU.JCL"

JCL_TEMP_MEMBERNAME = "TMP"

MOCK_SUBCMD_JCL_NO_DSNAME = """//MOCKPY JOB 'MOCK PYIPCS',CLASS=A
//*====================================================================  
//* MOCK PYIPCS SUBCOMMAND OBJECT JCL
//*====================================================================  
//IPCS EXEC PGM=IKJEFT01,DYNAMNBR=1000,REGION=0M                         
//IPCSDDIR DD DISP=SHR,DSN={ddir}
{allocations_jcl}
//SYSUDUMP DD SYSOUT=*         
//SYSTSPRT  DD DSN={mock_subcmd_dsname},DISP=OLD
//SYSTSIN DD * 
PROFILE MSGID 
IPCS NOPARM 
SETDEF NODSNAME LIST NOCONFIRM
{subcmds}
END   
"""

MOCK_SUBCMD_JCL_DSNAME = """//MOCKPY JOB 'MOCK PYIPCS',CLASS=A
//*====================================================================  
//* MOCK PYIPCS SUBCOMMAND OBJECT JCL
//*====================================================================  
//IPCS EXEC PGM=IKJEFT01,DYNAMNBR=1000,REGION=0M                         
//IPCSDDIR DD DISP=SHR,DSN={ddir}
{allocations_jcl}
//SYSUDUMP DD SYSOUT=*         
//SYSTSPRT  DD DSN={mock_subcmd_dsname},DISP=OLD
//SYSTSIN DD * 
PROFILE MSGID 
IPCS NOPARM 
SETDEF DSN('{dsname}') LIST NOCONFIRM
{subcmds}
END   
"""


def jcl_to_mock_subcmd(
    test_subcmds: list[str],
    test_allocations: dict[str, str | list[str]],
    test_ddir: str,
    test_dsname: str = "",
):
    """
    Uses JCL to create MockSubcmd objects

    Args:
        test_subcmds (list[str])
        test_allocations (dict[str,str|list[str]])
        test_ddir (str)
        test_dsname (str):
            Optional.
            Use dsname string to specify 'SETDEF DSNAME..' (Run dump against particular dump).
            Default is to empty string for 'SETDEF NODSNAME..'.
    Returns:
        list[MockSubcmd]: list of mock Subcmd objects where 'test_subcmds[i]'
            corresponds to 'returned_list[i]'
    """

    def format_allocations(allocations):
        allocations_str = ""
        for dd_name, specification in allocations.items():
            if specification:
                allocations_str += f"//{dd_name}  DD DSN={specification[0]},DISP=SHR\n"
            for dsname in specification[1:]:
                allocations_str += f"//         DD DSN={dsname},DISP=SHR\n"
        return allocations_str[:-1]

    def submit_jcl(jcl):
        jcl_dsname = TEST_HLQ + JCL_TEMP_DSNAME
        jcl_membername = f"{jcl_dsname}({JCL_TEMP_MEMBERNAME})"

        # create and write JCL to data set
        datasets.write(dataset_name=jcl_membername, content=jcl)

        # submit job
        job = jobs.submit(jcl_membername)
        job.wait()
        job.refresh()

        rc = datasets.delete(jcl_dsname)
        if rc != 0:
            warnings.warn(
                f"Mock pyIPCS Dataset To Write JCL '{jcl_membername}' Not Deleted",
                UserWarning,
            )

    mock_subcmd_dsname = TEST_HLQ + ".SUBCMD.MOCKJCL"
    datasets.write(mock_subcmd_dsname, "")

    allocations_jcl = format_allocations(test_allocations)

    jcl_subcmds = ""
    for test_subcmd in test_subcmds:
        jcl_subcmds = f"{jcl_subcmds}{test_subcmd}\n"
    jcl_subcmds = jcl_subcmds[:-1]

    if test_dsname:
        submit_jcl(
            MOCK_SUBCMD_JCL_DSNAME.format(
                ddir=test_ddir,
                allocations_jcl=allocations_jcl if allocations_jcl else "//*",
                mock_subcmd_dsname=mock_subcmd_dsname,
                dsname=test_dsname,
                subcmds=jcl_subcmds,
            )
        )
    else:
        submit_jcl(
            MOCK_SUBCMD_JCL_NO_DSNAME.format(
                ddir=test_ddir,
                allocations_jcl=allocations_jcl if allocations_jcl else "//*",
                mock_subcmd_dsname=mock_subcmd_dsname,
                subcmds=jcl_subcmds,
            )
        )

    job_output = datasets.read(mock_subcmd_dsname)
    rc = datasets.delete(mock_subcmd_dsname)
    if rc != 0:
        warnings.warn(
            f"Mock pyIPCS Dataset To Write JCL Subcommand Output '{mock_subcmd_dsname}'"
            + " Not Deleted",
            UserWarning,
        )

    # ==============================
    # Parse Output
    # ==============================

    mock_subcmd_list = []
    subcmd_index = job_output.find(f"\nIPCS\n{test_subcmds[0]}\n") + len(
        f"\nIPCS\n{test_subcmds[0]}\n"
    )
    # pylint: disable=consider-using-enumerate
    for i in range(len(test_subcmds)):
        if i != len(test_subcmds) - 1:
            subcmd_end_index = job_output.find(
                f"\nIPCS\n{test_subcmds[i+1]}\n", subcmd_index
            )
            mock_subcmd_list.append(
                MockSubcmd(
                    job_output[subcmd_index:subcmd_end_index],
                    mock_subcmd=test_subcmds[i],
                )
            )
            subcmd_index = subcmd_end_index + len(f"\nIPCS\n{test_subcmds[i+1]}\n")
        else:
            subcmd_end_index = job_output.find("\nIPCS\n", subcmd_index)
            mock_subcmd_list.append(
                MockSubcmd(
                    job_output[subcmd_index:subcmd_end_index],
                    mock_subcmd=test_subcmds[i],
                )
            )

    return mock_subcmd_list
