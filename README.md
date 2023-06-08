# AnimationEventImport

This is old code from my blog. I decided to move it to github to make it easier to find. It was originally written for a Unity version <5.0, and Blender version <3.0, so this will need some cleanup/updating.

Importing Animation Events from Blender into Unity3D
A question that comes up often in Unity3D support forums is how to import animation events from an application. There is no built in way to do this, but it is possible create a custom system by adding an exporter and importer for animation events yourself, in this example for Blender.

Installation into Blender
Open “File/User Preferences…” and the “Addons” panel.
Addon Preferences screen
Addon Preferences screen

Select “Install from file…” and open “Assets\Blender\io_anim_events.zip” from the project you installed the package into
If you can’t easily see the new addon enable the “Import Export” category
Enable “Export Animation Events”
Save your settings
The File/Export menu should now have an “Anim Events (.xml)” entry. The default import script looks for events with the name modelname.events.xml, but you can adjust the import script to use a different naming convention if that suits your workflow better.

Set up in Blender
Blender supports both Timeline Markers, which are part of the scene, and Pose Markers, which are part of an action. The import script only looks for pose markers, but the timeline markers are exported as well. I assume you set up your Blender scene to have one action for each animation, so that they are imported as separate animations into Unity3D.

Blender Markers
Blender Markers

By default markers in Blender are created on the timeline, but when “Show Pose Markers” is enabled in the action editor markers are created as part of the action. Pose markers show up as tiny diamonds in the dope sheet, while timeline markers are displayed as tiny triangles. The marker name needs to be appropriate for the animation event you want to trigger. In my example implementation I just write them out in a similar format as they are displayed in Unity’s animation editor, but it is possible to just reserve a few keywords that the importer then processes into animation events.

The example exporter writes to an XML file, but it is equally possible to use csv or plain text files.

<?xml version="1.0" ?>
<scene fps="24" version="1">
    <timeline>
        <markers>
            <marker frame="77" name="TimeLineMarker"/>
        </markers>
    </timeline>
    <actions>
        <action name="Alpha">
            <markers>
                <marker frame="5" name="Banana(1)"/>
                <marker frame="20" name="Raspberry(&quot;Pi&quot;)"/>
                <marker frame="10" name="Pear(1.0)"/>
            </markers>
        </action>
        <action name="Beta">
            <markers>
                <marker frame="0" name="Apple()"/>
            </markers>
        </action>
        <action name="CubeAction">
            <markers/>
        </action>
        <action name="Gamma">
            <markers/>
        </action>
    </actions>
</scene>
Import into Unity3D
I implemented three different import methods in Blender that are available from a preference pane.

Event Import Preferences
Event Import Preferences

Import XML looks for modelname.events.xml and applies the events in that file to the animations of a model during import.
Import Asset looks for modelname.events.asset . This can be used if you don’t want to specify animation events in Blender. To get an empty asset you need to select the model in the project view and select “Window/Add Event Data”. For production use it would be worth wrapping the class with a custom editor.
Import Automatic runs Blender in the background, exports animation events into the temporary directory and imports them right away into the model. This only works with .blend files. To make this work you need to specify the path to the Blender executable.
This is implemented by adding an AssetPostprocessor with OnPostprocessModel handler that is called whenever a model is imported in Unity. At the point when the handler is called the model and animation data is still writable, so it loads the event descriptions from a second file (modelname.events.xml or modelname.events.asset) and adds them to the appropriate animations.

I would use the automatic import if models are kept as .blend file in the project, the XML import if models are manually exported into .FBX files, and the asset importer if the animation tool doesn’t support events.

Example event handler
Animation events need to be received by a behaviour. This example behaviour is added automatically by the asset postprocessor, so each team will most likely want to customise it for their projects.

public class EventReceiver : MonoBehaviour {
    public void Apple() {
        Debug.Log ("Apple()");
    }
    public void Banana(int i) {
        Debug.Log (String.Format ("Banana({0})", i));
    }
    public void Pear(float f) {
        Debug.Log (String.Format ("Pear({0})", f));
    }
    public void Raspberry(string s) {
        Debug.Log (String.Format ("Raspberry({0})", s));
    }
}

Other options for automatic export
Running Blender from the asset postprocessor is the least invasive method, but requires Blender to be run twice, once for exporting the FBX and once for the animation events. An alternative is to run the animation event exporter whenever an FBX is exported, either from the Blender side or the Unity side.

The Blender script to export FBX lives at “Program Files\Blender Foundation\Blender\version\scripts\addons\io_scene_fbx\export_fbx.py” and the Unity3D script to run Blender is at “Program Files\Unity\Editor\Data\Tools\Unity-BlenderToFBX.py”. Though customising these scripts may mean more work across a big team or when updating Unity or Blender.

Another option is to keep Blender running in the background and sending commands to it, similar to how the Max and Maya pipelines work in Unity3D.

Mecanim
Mecanim has an interface to add events during import so I modified my scripts to add new events to events specified this way. Unfortunately there doesn’t seem to be an official API to get the imported animation clips when using mecanim. I’m using Object.FindObjectsOfType (typeof(AnimationClip)) which picks up some other animation clip objects as well, and there doesn’t seem to be a way to identify which belong to the import. At the moment I rely on clip names not having any conflicts. Please let me know if you run into problems.