from rnamake import motif
from rnamake import resource_manager as rm

m = motif.file_to_motif("../../data/ggaa_models/GGAA_tetraloop_round2_model221.motif")
rm.manager.add_motif(motif=m)

m_new = rm.manager.get_motif(name="new_ggaa_tetraloop", end_name="A7-A22")
m_new.to_pdb("test2.pdb")
m_org = rm.manager.get_motif(name="GGAA_tetraloop", end_name="A7-A22")
m_org.to_pdb("org.pdb")