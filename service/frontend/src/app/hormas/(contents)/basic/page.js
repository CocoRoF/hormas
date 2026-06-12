import SidebarAdmin from "@/app/hormas/components/SidebarAdmin"
import HormasDemo from "@/app/hormas/components/HormasDemo";

export default function BasicHormasPage() {
    return (
        <>
            <main id="main" role="main">
                <SidebarAdmin />
                <HormasDemo />
            </main>
        </>
    );
}